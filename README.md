# Digital Humanities Lab 網站

靜態網站包含 Home、About、Projects、Publications、Docs。源頁面在 `content/`，共用外觀在 `assets/site.css`，`assets/banner.png` 是原創水墨素材。執行 `node build.js` 可產生 `dist/`。

建議獨立 GitHub 倉庫以 GitHub Actions 從源碼產生 Pages 網站，保持聊齋地圖倉庫獨立。可在 GitHub 網頁編輯 `content/` 的 HTML 並提交，Actions 發布後所有設備看到同一版本；編輯前需登入並有倉庫權限。提交可在 GitHub 歷史中查看與回滾。

純靜態網站不會自動把讀者在瀏覽器上的地圖修訂寫進倉庫；目前地圖仍需匯出修訂並上傳 GitHub。WordPress 原頁面尚未遷移，老子資料暫時鏈接至原站。
