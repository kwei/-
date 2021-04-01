# **使用指南**

---

### 安裝套件

1. python-dotenv
2. selenium

### 使用前設定須知

1. 於 .env 檔中編輯 portal帳號與密碼
   * ACCOUNT=student id
   * PASSWORD=password
2. 於 .env 檔中編輯 chromedriver.exe. 的路徑 (須注意 chromedriver 版本)
   * /usr/local/bin/chromedriver (這是mac的路徑)
   * ./chromedriver (這是本地資料夾的路徑)
3. 於 .env 檔中編輯打卡時間的起始與終點 (24進制)
   * START_TIME=開始打卡時間
   * END_TIME=打卡結束時間
4. 於 .env 檔中編輯打卡時數
   * HOURS=時數要求

```
ACCOUNT={Portal 帳號}
PASSWORD={Portal 密碼}
WEBDRIVER_PATH={Driver 路徑}
START_TIME={打卡開始時間}
END_TIME={打卡結束時間}
HOURS={打卡時數要求}
```