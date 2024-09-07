# import Quartz
# from Foundation import NSScreen

# def get_display_scaling():
#     # Ruft Informationen zum Hauptbildschirm ab
#     screen = NSScreen.mainScreen()
#     description = screen.deviceDescription()
#     display_id = description.objectForKey_("NSScreenNumber")
#     display_info = Quartz.CGDisplayScreenSize(display_id)
    
#     # Ermittlung der physischen und virtuellen Auflösung
#     physical_width, physical_height = display_info.width, display_info.height
#     virtual_width = screen.frame().size.width
#     virtual_height = screen.frame().size.height

#     # Berechnen des Skalierungsfaktors
#     scaling_factor = physical_width / virtual_width
#     return scaling_factor

# scaling_factor = get_display_scaling()
# print(f"Skalierungsfaktor: {scaling_factor}")
