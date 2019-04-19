#
# registers_map contains a map of all VL53L0X registers
# Translated from the C library
# Date: 04/19/19
#

"""device registers"""

VL53L0X_DEFAULT_ADDRESS = 0x29

VL53L0X_REG_SYSRANGE_START = 0x000
VL53L0X_REG_SYSRANGE_MODE_MASK = 0x0F
VL53L0X_REG_SYSRANGE_MODE_START_STOP = 0x01
VL53L0X_REG_SYSRANGE_MODE_SINGLESHOT = 0x00
VL53L0X_REG_SYSRANGE_MODE_BACKTOBACK = 0x02
VL53L0X_REG_SYSRANGE_MODE_TIMED = 0x04
VL53L0X_REG_SYSRANGE_MODE_HISTOGRAM = 0x08

VL53L0X_REG_SYSTEM_THRESH_HIGH = 0x000C
VL53L0X_REG_SYSTEM_THRESH_LOW = 0x000E

VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG = 0x0001
VL53L0X_REG_SYSTEM_RANGE_CONFIG = 0x0009
VL53L0X_REG_SYSTEM_INTERMEASUREMENT_PERIOD = 0x0004

VL53L0X_REG_SYSTEM_INTERRUPT_CONFIG_GPIO = 0x000A
VL53L0X_REG_SYSTEM_INTERRUPT_GPIO_DISABLED = 0x00
VL53L0X_REG_SYSTEM_INTERRUPT_GPIO_LEVEL_LOW = 0x01
VL53L0X_REG_SYSTEM_INTERRUPT_GPIO_LEVEL_HIGH = 0x02
VL53L0X_REG_SYSTEM_INTERRUPT_GPIO_OUT_OF_WINDOW = 0x03
VL53L0X_REG_SYSTEM_INTERRUPT_GPIO_NEW_SAMPLE_READY = 0x04

VL53L0X_REG_GPIO_HV_MUX_ACTIVE_HIGH = 0x0084

VL53L0X_REG_SYSTEM_INTERRUPT_CLEAR = 0x000B

"""result registers"""

VL53L0X_REG_RESULT_INTERRUPT_STATUS = 0x0013
VL53L0X_REG_RESULT_RANGE_STATUS = 0x0014

VL53L0X_REG_RESULT_CORE_PAGE = 1
VL53L0X_REG_RESULT_CORE_AMBIENT_WINDOW_EVENTS_RTN = 0x00BC
VL53L0X_REG_RESULT_CORE_RANGING_TOTAL_EVENTS_RTN = 0x00C0
VL53L0X_REG_RESULT_CORE_AMBIENT_WINDOW_EVENTS_REF = 0x00D0
VL53L0X_REG_RESULT_CORE_RANGING_TOTAL_EVENTS_REF = 0x00D4
VL53L0X_REG_RESULT_PEAK_SIGNAL_RATE_REF = 0x00B6

"""algo registers"""

VL53L0X_REG_ALGO_PART_TO_PART_RANGE_OFFSET_MM = 0x0028

VL53L0X_REG_I2C_SLAVE_DEVICE_ADDRESS = 0x008a

"""check limit registers"""

VL53L0X_REG_MSRC_CONFIG_CONTROL = 0x0060

VL53L0X_REG_PRE_RANGE_CONFIG_MIN_SNR = 0X0027
VL53L0X_REG_PRE_RANGE_CONFIG_VALID_PHASE_LOW = 0x0056
VL53L0X_REG_PRE_RANGE_CONFIG_VALID_PHASE_HIGH = 0x0057
VL53L0X_REG_PRE_RANGE_MIN_COUNT_RATE_RTN_LIMIT = 0x0064

VL53L0X_REG_FINAL_RANGE_CONFIG_MIN_SNR = 0X0067
VL53L0X_REG_FINAL_RANGE_CONFIG_VALID_PHASE_LOW = 0x0047
VL53L0X_REG_FINAL_RANGE_CONFIG_VALID_PHASE_HIGH = 0x0048
VL53L0X_REG_FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT = 0x0044

VL53L0X_REG_PRE_RANGE_CONFIG_SIGMA_THRESH_HI = 0X0061
VL53L0X_REG_PRE_RANGE_CONFIG_SIGMA_THRESH_LO = 0X0062

"""pre range registers"""

VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD = 0x0050
VL53L0X_REG_PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI = 0x0051
VL53L0X_REG_PRE_RANGE_CONFIG_TIMEOUT_MACROP_LO = 0x0052

VL53L0X_REG_SYSTEM_HISTOGRAM_BIN = 0x0081
VL53L0X_REG_HISTOGRAM_CONFIG_INITIAL_PHASE_SELECT = 0x0033
VL53L0X_REG_HISTOGRAM_CONFIG_READOUT_CTRL = 0x0055

VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD = 0x0070
VL53L0X_REG_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI = 0x0071
VL53L0X_REG_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_LO = 0x0072
VL53L0X_REG_CROSSTALK_COMPENSATION_PEAK_RATE_MCPS = 0x0020

VL53L0X_REG_MSRC_CONFIG_TIMEOUT_MACROP = 0x0046

VL53L0X_REG_SOFT_RESET_GO2_SOFT_RESET_N = 0x00bf
VL53L0X_REG_IDENTIFICATION_MODEL_ID = 0x00c0
VL53L0X_REG_IDENTIFICATION_REVISION_ID = 0x00c2

VL53L0X_REG_OSC_CALIBRATE_VAL = 0x00f8

# equivalent to a range sigma of 655.35mm
VL53L0X_SIGMA_ESTIMATE_MAX_VALUE = 65535

VL53L0X_REG_GLOBAL_CONFIG_VCSEL_WIDTH = 0x032
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_0 = 0x0B0
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_1 = 0x0B1
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_2 = 0x0B2
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_3 = 0x0B3
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_4 = 0x0B4
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_5 = 0x0B5

VL53L0X_REG_GLOBAL_CONFIG_REF_EN_START_SELECT = 0xB6
VL53L0X_REG_DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD = 0x4E
VL53L0X_REG_DYNAMIC_SPAD_REF_EN_START_OFFSET = 0x4F
VL53L0X_REG_POWER_MANAGEMENT_GO1_POWER_FORCE = 0x80

# speed of light in um per 1E-10 seconds
VL53L0X_SPEED_OF_LIGHT_IN_AIR = 2997

VL53L0X_REG_VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV = 0x0089

VL53L0X_REG_ALGO_PHASECAL_LIM = 0x0030
VL53L0X_REG_ALGO_PHASECAL_CONFIG_TIMEOUT = 0x0030
