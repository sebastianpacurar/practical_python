io_kit_objects = [
    'AppleSmartBattery', 'IOBluetoothDevice', 'IOUSBDevice',
    'IOHIDevice', 'IOPCIDevice',
    'IOPowerSource', 'IOSerialBSDClient', 'IODisplayConnect', 'IOMedia',
    'IOPlatformExpertDevice', 'AppleRTC', 'IOUSBHostDevice', 'IONetworkInterface'
]

debug = ['SPSecureElementDataType']

long_ones = ['SPApplicationsDataType', 'SPInstallHistoryDataType', 'SPRawCameraDataType']

no_values = ['SPParallelATADataType', 'SPDeveloperToolsDataType', "SPDiagnosticsDataType", "SPDisabledSoftwareDataType",
             "SPDiscBurningDataType", "SPEthernetDataType", "SPFibreChannelDataType", "SPFireWireDataType",
             "SPLegacySoftwareDataType", "SPNetworkLocationDataType", 'SPPCIDataType', 'SPParallelSCSIDataType', 'SPPrefPaneDataType',
             'SPStartupItemDataType', 'SPWWANDataType']

might_not_use = ['SPAirPortDataType', 'SPExtensionsDataType', 'SPFrameworksDataType', 'SPLogsDataType', 'SPPrintersSoftwareDataType',
                 'SPPrintersDataType', 'SPConfigurationProfileDataType', "SPSASDataType", "SPSerialATADataType",
                 'SPSmartCardsDataType', 'SPSyncServicesDataType', 'SPThunderboltDataType']

not_nested = ['SPUniversalAccessDataType', 'SPSecureElementDataType', 'SPCameraDataType', 'SPiBridgeDataType',
              'SPMemoryDataType', 'SPSPIDataType', 'SPSoftwareDataType', 'SPNetworkVolumeDataType']

nested_1 = ['SPAudioDataType', 'SPFirewallDataType', 'SPFontsDataType', 'SPDisplaysDataType', 'SPHardwareDataType',
            'SPManagedClientDataType', 'SPStorageDataType', 'SPUSBDataType']

nested_with_info = ['SPBluetoothDataType', 'SPCardReaderDataType']

complex = ['SPInternationalDataType', 'SPNVMeDataType', 'SPNetworkDataType', 'SPPowerDataType']
