@echo off
setlocal enabledelayedexpansion

call pyuic5.bat "./forms/Dialog_Ask_Experiment_ID.ui" -o "./forms/Dialog_Ask_Experiment_ID_ui.py"
call pyuic5.bat "./forms/Dialog_Edit_Form.ui" -o "./forms/Dialog_Edit_Form_ui.py"
call pyuic5.bat "./forms/Dialog_Set_Initial.ui" -o "./forms/Dialog_Set_Initial_ui.py"
call pyuic5.bat "./forms/MainWindow.ui" -o "./forms/MainWindow_ui.py"
call pyuic5.bat "./forms/Widget_Each_Files_Information.ui" -o "./forms/Widget_Each_Files_Information_ui.py"
call pyuic5.bat "./forms/Widget_Equipment_Information.ui" -o "./forms/Widget_Equipment_Information_ui.py"
call pyuic5.bat "./forms/Widget_Experiment_Information.ui" -o "./forms/Widget_Experiment_Information_ui.py"
call pyuic5.bat "./forms/Widget_Sample_Information.ui" -o "./forms/Widget_Sample_Information_ui.py"
