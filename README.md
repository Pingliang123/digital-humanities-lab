# Digital Humanities Lab 網站

靜態網站包含 Home、About、Projects、Publications、Docs。源頁面在 `content/`，共用外觀在 `assets/site.css`，`assets/banner.png` 是原創水墨素材。執行 `node build.js` 可產生 `dist/`。

建議獨立 GitHub 倉庫以 GitHub Actions 從源碼產生 Pages 網站，保持聊齋地圖倉庫獨立。可在 GitHub 網頁編輯 `content/` 的 HTML 並提交，Actions 發布後所有設備看到同一版本；編輯前需登入並有倉庫權限。提交可在 GitHub 歷史中查看與回滾。

《老子》五個研究頁面與三篇相關文章已遷入 `content/laozi-*.html`，14 份圖片與附件保存於 `assets/laozi/`。`wordpress-source.json` 保留遷移時的原文、來源與附件校驗值。Google Drive、Kaggle 等外部資源保留原連結。手動執行 `python import_wordpress.py` 會重新取回並覆寫老子遷移頁面，日常編輯不應重跑。

《聊齋》地圖使用自己的資料倉庫；地圖內的雲端同步入口可授權保存人工修訂。GitHub 令牌僅留於當次地圖頁面記憶體，不會放進網站或提交。
