Set objShell = CreateObject("Wscript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get current folder path
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Build python command
pythonExe = "py"
launcher = """" & currentDir & "\Luncher.py" & """"

' First try py
On Error Resume Next
objShell.Run pythonExe & " -3 " & launcher, 0, False
If Err.Number <> 0 Then
    Err.Clear
    ' Try python
    pythonExe = "python"
    objShell.Run pythonExe & " " & launcher, 0, False
    If Err.Number <> 0 Then
        MsgBox "Python was not found on this system." & vbCrLf & "Please install Python 3.10+ and try again.", vbCritical, "Python Missing"
    End If
End If
