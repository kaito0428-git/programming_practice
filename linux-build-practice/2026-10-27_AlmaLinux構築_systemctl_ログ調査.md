# 2026-10-27 AlmaLinux 9.8 検証サーバ構築 / systemctl / ログ調査

## 目的
- ミドルウェアの構築・運用経験を積むための検証環境を自宅PCに作る
- Linuxの基本運用（サービス管理・ログ調査）を実機で体験する

---

## 1. 環境構成

| 項目 | 内容 |
|---|---|
| ホストOS | Windows 11 Pro（Ryzen 9 9900X / メモリ32GB） |
| 仮想化 | VirtualBox |
| VM名 / ホスト名 | mw01 |
| ゲストOS | AlmaLinux 9.8（minimal ISO, 最小限のインストール） |
| CPU / メモリ / ディスク | 2コア / 4GB / 40GB |
| NIC1（enp0s3） | NAT（インターネット接続用）10.0.2.15/24 |
| NIC2（enp0s8） | ホストオンリー（Windowsからの接続用）192.168.56.11/24 固定 |
| ユーザー | kaito（管理者 / sudo可）、rootのパスワードSSHログインは不可 |
| 接続方法 | Tera Term 5.7.1 から SSH（ポート22） |

### スナップショット
1. `OSインストール直後`
2. `初期設定後`（dnf update・再起動後）

---

## 2. 構築手順（概要）

1. AlmaLinux 公式サイトから `AlmaLinux-9.8-x86_64-minimal.iso` をダウンロード
2. VirtualBox で VM 作成（ISOは後から「設定 → ストレージ」で割り当て）
3. 「設定 → ネットワーク → アダプター2」でホストオンリーアダプターを有効化
4. インストーラで以下を設定
   - キーボード：日本語 / タイムゾーン：アジア/東京
   - enp0s3：ON（DHCP）
   - enp0s8：ON、IPv4 手動 `192.168.56.11/24`（ゲートウェイなし）
   - ホスト名：mw01
   - root パスワード設定、ユーザー kaito を管理者として作成
5. インストール後、Tera Term で SSH 接続を確認
   ```
   hostname      # mw01
   ip -br a      # enp0s8 に 192.168.56.11/24
   ```
6. 初期設定
   ```
   sudo dnf -y update
   timedatectl          # Time zone: Asia/Tokyo, NTP active を確認
   sudo reboot
   uname -r             # 5.14.0-687.60.1.el9_8.x86_64（新カーネルで起動）
   ```

---

## 3. トラブルシューティング記録

### (1) VM作成ウィザードで「完了」を押しても反応しない
- 原因：ISOを指定すると無人インストール設定の検証が走り、パスワード欄が空のため進めなかった
- 対処：ISOなしでVMを作成し、後から「設定 → ストレージ」でISOを割り当て

### (2) インストーラ起動時にカーネルが停止
- 症状1（CPU2）：`rcu: rcu_preempt detected stalls on CPUs/tasks`
- 症状2（CPU1）：`Kernel panic - not syncing: IO-APIC + timer doesn't work!`
- 原因：Windows の Hyper-V が有効で、VirtualBox が Hyper-V 上で動作しタイマー処理が不安定
- 対処：管理者コマンドプロンプトで Hyper-V を無効化し再起動
  ```
  bcdedit /set hypervisorlaunchtype off
  ```
  ※ 戻す場合は `bcdedit /set hypervisorlaunchtype auto`（WSL2/Docker利用時）
- 結果：CPU2・準仮想化デフォルトに戻して正常にインストール完了

### (3) 継続観察：VMのCPU停止と時刻ずれ
- `journalctl -p err -b` で `watchdog: BUG: soft lockup - CPU#1 stuck for 49s!` を確認（12:10:16）
- 同時刻に `Failed to start NTP client/server`（1回目の chronyd 起動が失敗）
- chronyd のログでも `System clock wrong by -52 seconds` が2回発生
- 推測：VMのCPUが数十秒止まり、その間に時計が遅れている（同一原因の可能性）
- 現状は自動復旧。再発確認用：
  ```
  journalctl -k | grep -i lockup
  chronyc tracking
  ```

---

## 4. systemctl によるサービス管理

```
systemctl status chronyd
sudo systemctl stop chronyd
sudo systemctl start chronyd
systemctl list-units --type=service --state=running
systemctl list-units --failed
```

### 学んだこと
| 項目 | 稼働中 | 停止後 |
|---|---|---|
| 先頭マーク | ● 緑 | ○ 白 |
| Active | active (running) | inactive (dead) |
| Loaded | enabled | enabled（変わらない） |
| Main PID | 734 | code=exited, status=0/SUCCESS |

- `stop` は「今止める」だけ。自動起動は `enabled` のまま → 起動時に自動で上げない場合は `disable`
- `status=0/SUCCESS` は正常終了。障害時は `failed` / 赤い ● になる
- 再起動後は PID が変わる（734 → 1967）。再起動確認は PID と since を見る
- 作業前後に `systemctl list-units --failed` で異常がないか確認する
- **sshd は止めない**（SSH接続できなくなる）

### 稼働中の主なサービス（14個）
sshd / crond / rsyslog / systemd-journald / firewalld / chronyd / auditd / NetworkManager など

---

## 5. ログ調査

### /var/log/secure（認証・sudo）
- Tera Term を2つ開き、片方で監視しながら、もう片方でわざとログイン失敗
  ```
  sudo tail -f /var/log/secure
  ```
- 記録例
  ```
  sshd-session[1986]: Failed password for kaito from 192.168.56.1 port 57387 ssh2
  sshd-session[1997]: Accepted password for kaito from 192.168.56.1 port 60513 ssh2
  sudo: kaito : TTY=pts/0 ; PWD=/home/kaito ; USER=root ; COMMAND=/bin/systemctl start chronyd
  ```
- ログイン時に `There were 2 failed login attempts since the last successful login.` と表示される

### 件数の集計と落とし穴
```
sudo grep "Failed password" /var/log/secure | wc -l      # 4件（想定は2件）
sudo grep "Failed password" /var/log/secure              # 中身を確認
sudo grep "Failed password for" /var/log/secure | wc -l  # 2件（正しい）
```
- 原因：sudo の実行記録（`COMMAND=/bin/grep Failed password ...`）自体が検索にヒットしていた
- 教訓：件数がおかしいときは `wc` を外して中身を目で確認する

### journalctl
```
journalctl -u sshd --since today    # サービス単位・期間で絞り込み
journalctl -p err -b                # 今回の起動以降のエラー以上
```

#### エラーの仕分け（journalctl -p err -b）
| ログ | 判定 |
|---|---|
| Unmaintained driver is detected: e1000 | 影響なし（仮想NICドライバの将来廃止予定警告） |
| vmwgfx ... unsupported hypervisor | 影響なし（GUI未使用） |
| rsyslogd: get tty ... failed | 影響なし |
| sudo: conversation failed | 原因判明（パスワード入力中に Ctrl+C） |
| soft lockup - CPU#1 stuck for 49s | 要調査（3-(3) 参照） |
| Failed to start NTP client/server | 要調査（同上） |

### /var/log/messages（システム全般）
```
sudo tail -n 20 /var/log/messages
```
- chronyd の起動、`dnf makecache`（systemd タイマーで約1時間おきに自動実行）、
  `New session 3 of user kaito`（secure の Accepted password と同時刻）などを確認

### ログの使い分け
| ログ | 内容 |
|---|---|
| /var/log/secure | ログイン・sudo など認証/セキュリティ |
| /var/log/messages | サービス起動停止などシステム全般 |
| journalctl | 上記をまとめて、サービス名・重要度・期間で絞り込み可能 |

---

## 6. ミスと気づき
- `wc -1`（数字）/ `wc -I`（大文字アイ）→ 正しくは `wc -l`（小文字エル = lines）
- `Faild` / `taill` などのタイポ → エラーメッセージ（`invalid option -- 'I'`、`command not found`）で原因特定
- sudo のパスワード入力中は画面に何も表示されない（止まっているわけではない）

---

## 7. 面談で話す用まとめ
> 自宅の検証環境（VirtualBox + AlmaLinux 9.8）を構築し、Tera Term から SSH 接続して運用しています。
> 構築時に Hyper-V 起因のカーネルパニックが発生しましたが、エラーメッセージからタイマー処理の問題と判断し、Hyper-V を無効化して解決しました。
> 運用面では systemctl によるサービスの停止・起動・状態確認、/var/log/secure を tail -f で監視しながらの SSH ログイン失敗の確認、grep での件数集計を行いました。
> 集計時に sudo の実行記録自体が検索に一致して件数が多く出たため、中身を確認して検索条件を見直しました。
> また journalctl -p err でエラーを洗い出し、影響なし・原因判明・要調査に仕分けました。

---

## 次回：Step 1-③ cron
- crontab で定期実行ジョブを作成し、`/var/log/cron` で実行を確認する
