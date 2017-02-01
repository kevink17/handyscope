from tiepie.library import libtiepie
from tiepie.deviceList import device_list
from datetime import date
import ctypes


class Device:
    def __init__(self, instr_id, id_kind, device_type):
        self._dev_handle = device_list.open_device(instr_id, id_kind, device_type)

    def __del__(self):
        libtiepie.DevClose(self._dev_handle)

    @property
    def driver_ver(self):
        raw_version = libtiepie.DevGetDriverVersion(self._dev_handle)
        return version_to_str(raw_version)

    @property
    def firmware_ver(self):
        raw_version = libtiepie.DevGetFirmwareVersion(self._dev_handle)
        return version_to_str(raw_version)

    @property
    def calibration_date(self):
        raw_date = libtiepie.DevGetCalibrationDate(self._dev_handle)
        split_date = date(raw_date >> 16, (raw_date >> 8) & 0xff, raw_date & 0xff)
        return split_date

    @property
    def serial_no(self):
        return libtiepie.DevGetSerialNumber(self._dev_handle)

    @property
    def product_id(self):
        id_int = libtiepie.DevGetProductId(self._dev_handle)

        # Lookup id in the dict
        for key in device_list.PRODUCT_IDS:
            if device_list.PRODUCT_IDS[key] == id_int:
                # Return human readable string, i.e. the key name
                return key

        # If code hasn't returned yet, product id wasn't found
        raise ValueError("Unknown product id: %s" % id_int)

    @property
    def device_type(self):
        type_int = libtiepie.DevGetType(self._dev_handle)

        # Lookup type in the dict
        for key in device_list.DEVICE_TYPES:
            if device_list.DEVICE_TYPES[key] == type_int:
                # Return human readable string, i.e. the key name
                return key

        # If code hasn't returned yet, device type wasn't found
        raise ValueError("Unknown device type: %s" % type_int)

    @property
    def long_name(self):
        # get length of device name string
        str_len = libtiepie.DevGetName(self._dev_handle, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.DevGetName(self._dev_handle, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    @property
    def name(self):
        # get length of device name string
        str_len = libtiepie.DevGetNameShort(self._dev_handle, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.DevGetNameShort(self._dev_handle, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    @property
    def short_name(self):
        # get length of device name string
        str_len = libtiepie.DevGetNameShortest(self._dev_handle, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.DevGetNameShortest(self._dev_handle, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    @property
    def is_removed(self):
        return libtiepie.DevIsRemoved(self._dev_handle) == 1

    def dev_close(self):
        libtiepie.DevClose(self._dev_handle)

    @property
    def trig_ins(self):
        # TODO implement class instantiation
        return None

    @property
    def trig_in_cnt(self):
        return libtiepie.DevTrGetInputCount(self._dev_handle)

    def trig_in_by_id(self, trig_in_id):
        # TODO implement trig_in_id dict
        libtiepie.DevTrGetInputIndexById(self._dev_handle, trig_in_id)

    @property
    def trig_outs(self):
        # TODO implement class instantiation
        return None

    @property
    def trig_out_cnt(self):
        return libtiepie.DevTrGetOutputCount(self._dev_handle)

    def trig_out_by_id(self, trig_out_id):
        # TODO implement trig_out_id dict
        libtiepie.DevTrGetOutputIndexById(self._dev_handle, trig_out_id)


def version_to_str(raw_version):
    return '.'.join([str((raw_version >> (idx * 16)) & 0xffff) for idx in range(3,-1,-1)])
