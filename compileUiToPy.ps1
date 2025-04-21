# ./form 内の *.ui ファイルを ./views に .py ファイルとして変換するスクリプト

# 変換元ディレクトリ
$sourceDir = "./forms"
# 変換先ディレクトリ
$targetDir = "./views"

# pyuic5 コマンドがインストールされているか確認
if (-not (Get-Command pyuic5 -ErrorAction SilentlyContinue)) {
    Write-Error "pyuic5 がインストールされていません。Python 環境にインストールしてください。"
    exit 1
}

# 変換先ディレクトリが存在しない場合は作成
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
}

# .ui ファイルを検索して変換
Get-ChildItem -Path $sourceDir -Filter "*.ui" | ForEach-Object {
    $uiFile = $_.FullName
    $pyFile = Join-Path $targetDir ($_.BaseName + ".py")

    # pyuic5 を使用して変換
    Write-Host "変換中: $uiFile -> $pyFile"
    pyuic5 -x $uiFile -o $pyFile
}

Write-Host "すべての .ui ファイルが変換されました。"
