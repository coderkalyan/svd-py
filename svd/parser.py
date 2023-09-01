from lxml import etree
import svd


access_map = {
    "read-write": svd.Access.READ_WRITE,
    "read-only": svd.Access.READ_ONLY,
    "write-only": svd.Access.WRITE_ONLY,
    "writeOnce": svd.Access.WRITE_ONCE,
    "read-writeOnce": svd.Access.READ_WRITE_ONCE,
}


protection_map = {
    "s": svd.Protection.SECURE,
    "n": svd.Protection.NON_SECURE,
    "p": svd.Protection.PRIVILEGED,
}

sau_region_access_map = {
    "n": svd.SAURegionAccess.NON_SECURE,
    "c": svd.SAURegionAccess.SECURE,
}


endian_map = {
    "little": svd.Endian.LITTLE,
    "big": svd.Endian.BIG,
    "selectable": svd.Endian.SELECTABLE,
    "other": svd.Endian.OTHER,
}


bool_map = {
    "true": True,
    "false": False,
    "1": True,
    "0": False,
}


address_block_usage_map = {
    "registers": svd.AddressBlockUsage.REGISTERS,
    "buffer": svd.AddressBlockUsage.BUFFER,
    "reserved": svd.AddressBlockUsage.RESERVED,
}


data_type_map = {
    "uint8_t": svd.DataType.UINT8,
    "uint16_t": svd.DataType.UINT16,
    "uint32_t": svd.DataType.UINT32,
    "uint64_t": svd.DataType.UINT64,
    "int8_t": svd.DataType.INT8,
    "int16_t": svd.DataType.INT16,
    "int32_t": svd.DataType.INT32,
    "int64_t": svd.DataType.INT64,
    "uint8_t *": svd.DataType.UINT8_PTR,
    "uint16_t *": svd.DataType.UINT16_PTR,
    "uint32_t *": svd.DataType.UINT32_PTR,
    "uint64_t *": svd.DataType.UINT64_PTR,
    "int8_t *": svd.DataType.INT8_PTR,
    "int16_t *": svd.DataType.INT16_PTR,
    "int32_t *": svd.DataType.INT32_PTR,
    "int64_t *": svd.DataType.INT64_PTR,
}


write_operation_map = {
    "oneToClear": svd.WriteOperation.ONE_TO_CLEAR,
    "oneToSet": svd.WriteOperation.ONE_TO_SET,
    "oneToToggle": svd.WriteOperation.ONE_TO_TOGGLE,
    "zeroToClear": svd.WriteOperation.ZERO_TO_CLEAR,
    "zeroToSet": svd.WriteOperation.ZERO_TO_SET,
    "zeroToToggle": svd.WriteOperation.ZERO_TO_TOGGLE,
    "modify": svd.WriteOperation.MODIFY,
    "clear": svd.WriteOperation.CLEAR,
    "set": svd.WriteOperation.SET,
}


read_operation_map = {
    "clear": svd.ReadOperation.CLEAR,
    "modify": svd.ReadOperation.MODIFY,
    "set": svd.ReadOperation.SET,
    "modifyExternal": svd.ReadOperation.MODIFY_EXTERNAL,
}


class Parser:
    """Parses an SVD XML string into python objects."""

    @classmethod
    def convert(cls, content: str) -> svd.Device:
        """Initializes an svd.Device instance from an XML string"""

        root = etree.fromstring(bytes(bytearray(content, encoding='utf-8')))
        """
        for elem in root.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
            if elem.tail is not None:
                elem.tail = elem.tail.strip()
        """

        return Parser.parse_device(root)

    @classmethod
    def parse_device(cls, root):
        device = svd.Device()

        # required information
        if (value := root.find("name")) is not None:
            device.name = value.text
        else:
            raise KeyError("Unable to find key 'name'")
        if (value := root.find("version")) is not None:
            device.svd_version = value.text
        else:
            raise KeyError("Unable to find key 'version'")
        if (value := root.find("width")) is not None:
            device.width = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'width'")
        if (value := root.find("addressUnitBits")) is not None:
            device.address_unit_bits = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'addressUnitBits'")
        if (value := root.find("peripherals")) is not None:
            device.peripherals = cls.parse_peripherals(value)
        else:
            raise KeyError("Unable to find key 'peripherals'")

        # optional information
        if (value := root.find("vendor")) is not None:
            device.vendor = value.text
        if (value := root.find("vendorID")) is not None:
            device.vendor_id = value.text
        if (value := root.find("series")) is not None:
            device.series = value.text
        if (value := root.find("description")) is not None:
            device.description = value.text
        if (value := root.find("size")) is not None:
            device.size = int(value.text, 0)
        if (value := root.find("licenseText")) is not None:
            device.license_text = value.text
        if (value := root.find("access")) is not None:
            device.default_access = access_map[value.text]
        if (value := root.find("protection")) is not None:
            device.default_protection = protection_map[value.text]
        if (value := root.find("resetValue")) is not None:
            device.default_reset_value = int(value.text, 0)
        if (value := root.find("resetMask")) is not None:
            device.default_reset_mask = int(value.text, 0)

        if (value := root.find("cpu")) is not None:
            device.cpu = cls.parse_cpu(value)

        return device

    @classmethod
    def parse_cpu(cls, tree):
        cpu = svd.CPU()

        # required information
        if (value := tree.find("name")) is not None:
            cpu.name = value.text
        else:
            raise KeyError("Unable to find key 'name'")
        if (value := tree.find("revision")) is not None:
            cpu.revision = value.text
        else:
            raise KeyError("Unable to find key 'revision'")
        if (value := tree.find("endian")) is not None:
            cpu.endian = endian_map[value.text]
        else:
            raise KeyError("Unable to find key 'endian'")
        if (value := tree.find("mpuPresent")) is not None:
            cpu.mpu = bool_map[value.text]
        else:
            raise KeyError("Unable to find key 'mpuPresent'")
        if (value := tree.find("fpuPresent")) is not None:
            cpu.fpu = bool_map[value.text]
        else:
            raise KeyError("Unable to find key 'fpuPresent'")
        if (value := tree.find("nvicPrioBits")) is not None:
            cpu.nvic_priority_bits = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'nvicPrioBits'")
        if (value := tree.find("vendorSystickConfig")) is not None:
            cpu.vendor_systick = bool_map[value.text]
        else:
            raise KeyError("Unable to find key 'vendorSystickConfig'")

        # optional information
        if (value := tree.find("fpuDP")) is not None:
            cpu.fpu_double_precision = bool_map[value.text]
        if (value := tree.find("dspPresent")) is not None:
            cpu.dsp = bool_map[value.text]
        if (value := tree.find("icachePresent")) is not None:
            cpu.icache = bool_map[value.text]
        if (value := tree.find("dcachePresent")) is not None:
            cpu.dcache = bool_map[value.text]
        if (value := tree.find("itcmPresent")) is not None:
            cpu.itcm = bool_map[value.text]
        if (value := tree.find("dtcmPresent")) is not None:
            cpu.dtcm = bool_map[value.text]
        if (value := tree.find("vtorPresent")) is not None:
            cpu.vtor = bool_map[value.text]
        if (value := tree.find("deviceNumInterrupts")) is not None:
            cpu.num_interrupts = int(value.text, 0)
            
        # SAU Regions (optional)
        if (value := tree.find("sauNumRegions")) is not None:
            cpu.sau_num_regions = int(value.text, 0)
        if (value := tree.find("sauRegionsConfig")) is not None:
            cpu.sau_region_config = cls.parse_sau(value)

        return cpu

    @classmethod 
    def parse_sau(cls, tree):
        sau_config = svd.SAURegionConfig()
        
        attrib = tree.attrib
        if "enabled" in attrib:
            sau_config.enabled = bool_map[attrib["enabled"]]
        if "protectionWhenDisabled" in attrib:
            sau_config.protection = protection_map[attrib["protectionWhenDisabled"]]

        for node in tree.findall("region"):
            sau_config.sau_regions.append(cls.parse_sau_region(node))

        return sau_config

    @classmethod
    def parse_sau_region(cls, tree):
        sau_region = svd.SAURegion()

        attrib = tree.attrib
        if "enabled" in attrib:
            sau_region.enabled = bool_map[attrib["enabled"]]
        if "name" in attrib:
            sau_region.name = attrib["name"]

        if (value := tree.find("base")) is not None:
            sau_region.base_address = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'base' in SAU Region")
        if (value := tree.find("limit")) is not None:
            sau_region.limit_address = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'limit' in SAU Region")
        if (value := tree.find("access")) is not None:
            sau_region.access = sau_region_access_map[value.text]
        else:
            raise KeyError("Unable to find key 'access' in SAU Region")

        return sau_region
        
    @classmethod
    def parse_peripherals(cls, tree):
        peripherals = []

        i = 0
        for node in tree.findall("peripheral"):
            peripherals.append(cls.parse_peripheral(node))
            # if i == 0: print(etree.tostring(node))
            i += 1

        return peripherals

    @classmethod
    def parse_peripheral(cls, tree):
        peripheral = svd.Peripheral()

        # required information
        if (value := tree.find("name")) is not None:
            peripheral.name = value.text
        else:
            raise KeyError("Unable to find key 'name'")
        if (value := tree.find("baseAddress")) is not None:
            peripheral.base_address = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'baseAddress'")

        # optional information
        if (value := tree.find("version")) is not None:
            peripheral.svd_version = value.text
        if (value := tree.find("description")) is not None:
            peripheral.description = value.text
        if (value := tree.find("alternatePeripheral")) is not None:
            peripheral.alternate = value.text
        if (value := tree.find("groupName")) is not None:
            peripheral.group_name = value.text
        if (value := tree.find("prependToName")) is not None:
            peripheral.register_prefix = value.text
        if (value := tree.find("appendToName")) is not None:
            peripheral.register_suffxi = value.text
        if (value := tree.find("headerStructName")) is not None:
            peripheral.struct_name = value.text
        if (value := tree.find("disableCondition")) is not None:
            peripheral.disable_condition = value.text
        if (value := tree.find("access")) is not None:
            peripheral.default_access = access_map[value.text]
        if (value := tree.find("protection")) is not None:
            peripheral.default_protection = protection_map[value.text]
        if (value := tree.find("resetValue")) is not None:
            peripheral.default_reset_value = int(value.text, 0)
        if (value := tree.find("resetMask")) is not None:
            peripheral.default_reset_mask = int(value.text, 0)
        if (node := tree.find("addressBlock")) is not None:
            peripheral.address_block = cls.parse_address_block(node)
        else:
            peripheral.address_block = None
        if (node := tree.find("registers")) is not None:
            peripheral.registers = cls.parse_registers(node)

        for node in tree.findall("interrupt"):
            peripheral.interrupts.append(cls.parse_interrupt(node))

        return peripheral

    @classmethod
    def parse_address_block(cls, tree):
        address_block = svd.AddressBlock()

        # required information
        if (value := tree.find("offset")) is not None:
            address_block.offset = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'offset'")
        if (value := tree.find("size")) is not None:
            address_block.size = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'size'")
        if (value := tree.find("usage")) is not None:
            address_block.usage = address_block_usage_map[value.text]
        else:
            raise KeyError("Unable to find key 'usage'")

        # optional information
        if (value := tree.find("protection")) is not None:
            address_block.usage = protection_map[value.text]

        return address_block

    @classmethod
    def parse_interrupt(cls, tree):
        interrupt = svd.Interrupt()

        # required information
        if (value := tree.find("name")) is not None:
            interrupt.name = value.text
        else:
            raise KeyError("Unable to find key 'name'")
        if (value := tree.find("value")) is not None:
            interrupt.value = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'value'")

        # optional information
        if (value := tree.find("description")) is not None:
            interrupt.description = value.text

        return interrupt

    @classmethod
    def parse_registers(cls, tree):
        registers = []

        for node in tree.findall("register"):
            registers.append(cls.parse_register(node))

        return registers

    @classmethod
    def parse_register(cls, tree):
        register = svd.Register()

        # required information
        if (value := tree.find("name")) is not None:
            register.name = value.text
        else:
            raise KeyError("Unable to find key 'name'")
        if (value := tree.find("addressOffset")) is not None:
            register.address_offset = int(value.text, 0)
        else:
            raise KeyError("Unable to find key 'addressOffset'")

        if (value := tree.find("displayName")) is not None:
            register.display_name = value.text
        if (value := tree.find("description")) is not None:
            register.description = value.text
        if (value := tree.find("size")) is not None:
            register.size = int(value.text, 0)
        if (value := tree.find("access")) is not None:
            register.access = access_map[value.text]
        if (value := tree.find("protection")) is not None:
            register.protection = protection_map[value.text]
        if (value := tree.find("resetValue")) is not None:
            register.reset_value = int(value.text, 0)
        if (value := tree.find("resetMask")) is not None:
            register.reset_mask = int(value.text, 0)
        if (value := tree.find("dataType")) is not None:
            register.data_type = data_type_map[value.text]
        if (value := tree.find("modifiedWriteValues")) is not None:
            register.modify_operation = write_operation_map[value.text]
        if (value := tree.find("readAction")) is not None:
            register.read_operation = read_operation_map[value.text]
        if (node := tree.find("fields")) is not None:
            register.fields = cls.parse_fields(node)

        if len(register.fields) > 0:
            register.bits = 0
            for field in register.fields:
                register.bits |= field.bits

        return register

    @classmethod
    def parse_fields(cls, tree):
        fields = []

        for node in tree.findall("field"):
            fields.append(cls.parse_field(node))

        return fields

    @classmethod
    def parse_field(cls, tree):
        field = svd.Field()

        if (value := tree.find("name")) is not None:
            field.name = value.text
        else:
            raise KeyError("Unable to find key 'name'")
        if (value := tree.find("bitRange")) is not None:
            parsed = value.text[1:-1]
            field.bit_range = tuple(map(int, parsed.split(":")))
        elif (value := tree.find("lsb")) is not None:
            msb = tree.find("msb")
            assert msb is not None
            msb_val = int(msb.text, 0)
            lsb_val = int(value.text, 0)
            field.bit_range = (msb_val, lsb_val)
        elif (value := tree.find("bitOffset")) is not None:
            offset = int(value.text)
            value = tree.find("bitWidth")
            assert value is not None
            width = int(value.text)
            field.bit_range = (offset, offset + width - 1)
        else:
            cls.print_tree(tree)
            raise KeyError("Unable to find any keys for bit range definition")

        if (value := tree.find("access")) is not None:
            field.access = access_map[value.text]
        if (value := tree.find("modifiedWriteValues")) is not None:
            field.modify_operation = write_operation_map[value.text]
        if (value := tree.find("readAction")) is not None:
            field.read_operation = read_operation_map[value.text]
        if (value := tree.find("description")) is not None:
            field.description = value.text

        for i in range(field.bit_range[1], field.bit_range[0] + 1):
            field.bits |= (1 << i)

        return field
    
    @classmethod
    def print_tree(cls, tree):
        print(etree.tostring(tree, pretty_print=True, encoding='unicode'))
   
