import os

import oyaml as yaml

class GUI_Config():

  config = None

  G_LAYOUT = {}

  G_GUI_INDEX = {
    'boot':0,
    'main':1,
    'menu':2,
    'ANT+Top':3,
    'ANT+Detail':4,
    'Wheel Size':5,
    'Adjust Altitude':6,
    'Debug Log Viewer':7,
    #'log':5,
    #'setting':6,
  }

  G_UNIT ={
    "HeartRate":"{0:^.0f}bpm",
    "Cadence":"{0:^.0f}rpm",
    "Speed":"{0:^3.1f}km/h",
    "Distance":"{0:^3.1f}km",
    "Power":"{0:^4.0f}w",
    "Work":"{0:^4.0f}kJ",
    "Position":"{0:^3.5f}",
    "Altitude":"{0:^5.0f}m",
    "Grade":"{0:^2.0f}%",
    "GPS_error":"{0:^4.0f}m"
  }

  G_ITEM_DEF = {
    #integrated
    "Power":(G_UNIT["Power"],"self.sensor.values['integrated']['power']"),
    "Speed":(G_UNIT["Speed"],"self.sensor.values['integrated']['speed']"),
    "Dist.":(G_UNIT["Distance"],"self.sensor.values['integrated']['distance']"),
    "Cad.":(G_UNIT["Cadence"],"self.sensor.values['integrated']['cadence']"),
    "HR":(G_UNIT["HeartRate"],"self.sensor.values['integrated']['hr']"),
    "Work":(G_UNIT["Work"],"self.sensor.values['integrated']['accumulated_power']"),
    "Grade":(G_UNIT["Grade"],"self.sensor.values['integrated']['grade']"),
    "Grade(spd)":(G_UNIT["Grade"],"self.sensor.values['integrated']['grade_spd']"),
    "GlideRatio":("{0:.0f}m","self.sensor.values['integrated']['glide_ratio']"),
    #GPS raw
    "Latitude":(G_UNIT["Position"],"self.sensor.values['GPS']['lat']"),
    "Longitude":(G_UNIT["Position"],"self.sensor.values['GPS']['lon']"),
    "Alt.(GPS)":(G_UNIT["Altitude"],"self.sensor.values['GPS']['alt']"),
    "Speed(GPS)":(G_UNIT["Speed"],"self.sensor.values['GPS']['speed']"),
    "Dist.(GPS)":(G_UNIT["Distance"],"self.sensor.values['GPS']['distance']"),
    "Heading(GPS)":("{0:^s}","self.sensor.values['GPS']['track_str']"),
    "Satellites":("{0:^s}","self.sensor.values['GPS']['used_sats_str']"),
    "Error":(G_UNIT["GPS_error"],"self.sensor.values['GPS']['error']"),
    "Error(x)":(G_UNIT["GPS_error"],"self.sensor.values['GPS']['epx']"),
    "Error(y)":(G_UNIT["GPS_error"],"self.sensor.values['GPS']['epy']"),
    "GPSTime":("{0:^s}","self.sensor.values['GPS']['utctime']"),
    "GPS Fix":("{0:^d}","self.sensor.values['GPS']['mode']"),
    "Course Dist.":(G_UNIT["Distance"],"self.sensor.values['GPS']['course_distance']"),
    #ANT+ raw
    "HR(ANT+)":(G_UNIT["HeartRate"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['HR']]['hr']"),
    "Speed(ANT+)":(G_UNIT["Speed"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['SPD']]['speed']"),
    "Dist.(ANT+)":(G_UNIT["Distance"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['SPD']]['distance']"),
    "Cad.(ANT+)":(G_UNIT["Cadence"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['CDC']]['cadence']"),
    #get from sensor as powermeter pairing
    # (cannot get from other pairing not including power sensor pairing)
    "Power16(ANT+)":(G_UNIT["Power"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x10]['power']"),
    "Power16s(ANT+)":(G_UNIT["Power"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x10]['power_16_simple']"),
    "Cad.16(ANT+)":(G_UNIT["Cadence"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x10]['cadence']"),
    "Work16(ANT+)":(G_UNIT["Work"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x10]['accumulated_power']"),
    "Power R(ANT+)":(G_UNIT["Power"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x10]['power_r']"),
    "Power L(ANT+)":(G_UNIT["Power"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x10]['power_l']"),
    "Balance(ANT+)":("{0:^s}",\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x10]['lr_balance']"),
    "Power17(ANT+)":(G_UNIT["Power"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x11]['power']"),
    "Speed17(ANT+)":(G_UNIT["Speed"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x11]['speed']"),
    "Dist.17(ANT+)":(G_UNIT["Distance"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x11]['distance']"),
    "Work17(ANT+)":(G_UNIT["Work"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x11]['accumulated_power']"),
    "Power18(ANT+)":(G_UNIT["Power"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x12]['power']"),
    "Cad.18(ANT+)":(G_UNIT["Cadence"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x12]['cadence']"),
    "Work18(ANT+)":(G_UNIT["Work"],\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x12]['accumulated_power']"),
    "Torque Ef.(ANT+)":("{0:^s}",\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x13]['torque_eff']"),
    "Pedal Sm.(ANT+)":("{0:^s}",\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['PWR']][0x13]['pedal_sm']"),
    "Light(ANT+)":("{0:^s}",\
      "self.sensor.values['ANT+'][self.config.G_ANT['ID_TYPE']['LGT']]['lgt_state_display']"),
    #ANT+ multi
    "PWR1":(G_UNIT["Power"],"None"),
    "PWR2":(G_UNIT["Power"],"None"),
    "PWR3":(G_UNIT["Power"],"None"),
    "HR1":(G_UNIT["HeartRate"],"None"),
    "HR2":(G_UNIT["HeartRate"],"None"),
    "HR3":(G_UNIT["HeartRate"],"None"),
    #Sensor raw
    "Temp":("{0:^3.0f}C","self.sensor.values['I2C']['temperature']"),
    "Pressure":("{0:^4.0f}hPa","self.sensor.values['I2C']['pressure']"),
    "Altitude":(G_UNIT["Altitude"],"self.sensor.values['I2C']['altitude']"),
    "Accum.Alt.":(G_UNIT["Altitude"],"self.sensor.values['I2C']['accumulated_altitude']"),
    "Vert.Spd":("{0:^3.1f}m/s","self.sensor.values['I2C']['vertical_speed']"),
    "Ascent":(G_UNIT["Altitude"],"self.sensor.values['I2C']['total_ascent']"),
    "Descent":(G_UNIT["Altitude"],"self.sensor.values['I2C']['total_descent']"),
    "Light":("{0:^5.0f}","self.sensor.values['I2C']['light']"),
    "Motion":("{0:^1.1f}","self.sensor.values['I2C']['motion']"),
    "M_Stat":("{0:^1.1f}","self.sensor.values['I2C']['m_stat']"),
    "ACC_X":("{0:^1.1f}","self.sensor.values['I2C']['acc'][0]"),
    "ACC_Y":("{0:^1.1f}","self.sensor.values['I2C']['acc'][1]"),
    "ACC_Z":("{0:^1.1f}","self.sensor.values['I2C']['acc'][2]"),
    "Battery":("{0:^1.0f}%","self.sensor.values['I2C']['battery_percentage']"),
    "Heading":("{0:^s}","self.sensor.values['I2C']['heading_str']"),
    "Pitch":("{0:^1.0f}","self.sensor.values['I2C']['modified_pitch']"),
    #General
    "Timer":("timer","self.logger.values['count']"),
    "LapTime":("timer","self.logger.values['count_lap']"),
    "Lap":("{0:^d}","self.logger.values['lap']"),
    "Time":("time","0"),
    "ElapsedTime":("timer","self.logger.values['elapsed_time']"),
    "GrossAveSPD":(G_UNIT["Speed"],"self.logger.values['gross_ave_spd']"),
    "GrossDiffTime":("{0:^s}","self.logger.values['gross_diff_time']"),
    "CPU_MEM":("{0:^s}","self.sensor.values['CPU_MEM']"),
    #Statistics
    #Pre Lap Average or total
    "PLap HR":(G_UNIT["HeartRate"],"self.logger.record_stats['pre_lap_avg']['heart_rate']"),
    "PLap CAD":(G_UNIT["Cadence"],"self.logger.record_stats['pre_lap_avg']['cadence']"),
    "PLap DIST":(G_UNIT["Distance"],"self.logger.record_stats['pre_lap_avg']['distance']"),
    "PLap SPD":(G_UNIT["Speed"],"self.logger.record_stats['pre_lap_avg']['speed']"),
    "PLap PWR":(G_UNIT["Power"],"self.logger.record_stats['pre_lap_avg']['power']"),
    "PLap WRK":(G_UNIT["Work"],"self.logger.record_stats['pre_lap_avg']['accumulated_power']"),
    "PLap ASC":(G_UNIT["Altitude"],"self.logger.record_stats['pre_lap_avg']['total_ascent']"),
    "PLap DSC":(G_UNIT["Altitude"],"self.logger.record_stats['pre_lap_avg']['total_descent']"),
    #Lap Average or total
    "Lap HR":(G_UNIT["HeartRate"],"self.logger.record_stats['lap_avg']['heart_rate']"),
    "Lap CAD":(G_UNIT["Cadence"],"self.logger.record_stats['lap_avg']['cadence']"),
    "Lap DIST":(G_UNIT["Distance"],"self.logger.record_stats['lap_avg']['distance']"),
    "Lap SPD":(G_UNIT["Speed"],"self.logger.record_stats['lap_avg']['speed']"),
    "Lap PWR":(G_UNIT["Power"],"self.logger.record_stats['lap_avg']['power']"),
    "Lap WRK":(G_UNIT["Work"],"self.logger.record_stats['lap_avg']['accumulated_power']"),
    "Lap ASC":(G_UNIT["Altitude"],"self.logger.record_stats['lap_avg']['total_ascent']"),
    "Lap DSC":(G_UNIT["Altitude"],"self.logger.record_stats['lap_avg']['total_descent']"),
    #Entire Average
    "Ave HR":(G_UNIT["HeartRate"],"self.logger.record_stats['entire_avg']['heart_rate']"),
    "Ave CAD":(G_UNIT["Cadence"],"self.logger.record_stats['entire_avg']['cadence']"),
    "Ave SPD":(G_UNIT["Speed"],"self.logger.record_stats['entire_avg']['speed']"),
    "Ave PWR":(G_UNIT["Power"],"self.logger.record_stats['entire_avg']['power']"),
    #Max
    "Max HR":(G_UNIT["HeartRate"],"self.logger.record_stats['entire_max']['heart_rate']"),
    "Max CAD":(G_UNIT["Cadence"],"self.logger.record_stats['entire_max']['cadence']"),
    "Max SPD":(G_UNIT["Speed"],"self.logger.record_stats['entire_max']['speed']"),
    "Max PWR":(G_UNIT["Power"],"self.logger.record_stats['entire_max']['power']"),
    "LMax HR":(G_UNIT["HeartRate"],"self.logger.record_stats['lap_max']['heart_rate']"),
    "LMax CAD":(G_UNIT["Cadence"],"self.logger.record_stats['lap_max']['cadence']"),
    "LMax SPD":(G_UNIT["Speed"],"self.logger.record_stats['lap_max']['speed']"),
    "LMax PWR":(G_UNIT["Power"],"self.logger.record_stats['lap_max']['power']"),
    "PLMax HR":(G_UNIT["HeartRate"],"self.logger.record_stats['pre_lap_max']['heart_rate']"),
    "PLMax CAD":(G_UNIT["Cadence"],"self.logger.record_stats['pre_lap_max']['cadence']"),
    "PLMax SPD":(G_UNIT["Speed"],"self.logger.record_stats['pre_lap_max']['speed']"),
    "PLMax PWR":(G_UNIT["Power"],"self.logger.record_stats['pre_lap_max']['power']")
  }

  G_LANG = {
    "JA": {
      "Power":"パワー",
      "Speed":"スピード",
      "Dist.":"距離",
      "Cad.":"ケイデンス",
      "HR":"心拍",
      "Work":"仕事量",
      "Timer":"タイマー",
      "Ascent":"獲得標高",
      #"":"",
    },
  }

  def __init__(self, config):
    self.config = config
    
    #read layout
    if os.path.exists(self.config.G_LAYOUT_FILE):
      self.read_layout()

  def read_layout(self):
    text = None
    with open(self.config.G_LAYOUT_FILE) as file:
      text = file.read()
      self.G_LAYOUT = yaml.safe_load(text)

