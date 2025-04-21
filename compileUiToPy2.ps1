# ./form 内の *.ui ファイルを ./views に .py ファイルとして変換するスクリプト

# 変換元ディレクトリ
$sourceDir = "./forms"
# 変換先ディレクトリ
$targetDir = "./views"
# バックアップディレクトリ
$backupDir = "./views_backup"

# pyuic5 コマンドがインストールされているか確認
if (-not (Get-Command pyuic5 -ErrorAction SilentlyContinue)) {
    Write-Error "pyuic5 がインストールされていません。Python 環境にインストールしてください。"
    exit 1
}

# 変換先ディレクトリが存在しない場合は作成
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
}

# バックアップディレクトリが存在しない場合は作成
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
}

# .ui ファイルを検索して変換
Get-ChildItem -Path $sourceDir -Filter "*.ui" | ForEach-Object {
    $uiFile = $_.FullName
    $pyFile = Join-Path $targetDir ($_.BaseName + ".py")
    $backupFile = Join-Path $targetDir ($_.BaseName + "_tmp.py")

    # # 既存の .py ファイルをバックアップ
    # if (Test-Path $pyFile) {
    #     Copy-Item -Path $pyFile -Destination $backupFile -Force
    #     Write-Host "バックアップ作成: $pyFile -> $backupFile"
    # }

    # pyuic5 を使用して変換
    Write-Host "変換中: $uiFile -> $backupFile"
    pyuic5 -x $uiFile -o $backupFile

    # 既存の .py ファイルと新しい .py ファイルを比較してマージ
    if (Test-Path $backupFile) {
        $originalContent = Get-Content -Path $backupFile
        $newContent = Get-Content -Path $pyFile

        # 差分を検出
        $mergedContent = Compare-Object -ReferenceObject $originalContent -DifferenceObject $newContent -IncludeEqual | ForEach-Object {
            if ($_.SideIndicator -eq "==") {
                $_.InputObject  # 共通部分
            }
            elseif ($_.SideIndicator -eq "<=") {
                $_.InputObject # 新しい部分
            }
            elseif ($_.SideIndicator -eq "=>") {
                $_.InputObject # 古い部分（必要に応じて保持）
            }
        }

        # マージ結果を保存
        $mergedContent | Set-Content -Path $pyFile
        Write-Host "マージ完了: $pyFile"
        Remove-Item -Path $backupFile -Force
    }
}

Write-Host "すべての .ui ファイルが変換され、マージされました。"
