from enum import Enum


class Win32OSRecoveryConfiguration(Enum):
    AutoReboot = 'Auto Reboot'
    Caption = 'Caption'
    DebugFilePath = 'Debug File Path'
    DebugInfoType = 'Debug Info Type'
    Description = 'Description'
    ExpandedDebugFilePath = 'Expanded Debug File Path'
    ExpandedMiniDumpDirectory = 'Expanded Mini Dump Directory'
    KernelDumpOnly = 'Kernel Dump Only'
    MiniDumpDirectory = 'Mini Dump Directory'
    Name = 'Name'
    OverwriteExistingDebugFile = 'Overwrite Existing Debug File'
    SendAdminAlert = 'Send Admin Alert'
    SettingID = 'Setting ID'
    WriteDebugInfo = 'Write Debug Info'
    WriteToSystemLog = 'Write To System Log'
