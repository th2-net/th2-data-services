from th2_data_services.th2_gui_report import Th2GUIReport

gui = Th2GUIReport("http://th2-qa:30000/th2-commonv3/")
result_event_link = gui.get_event_link("fcace9a4-8fd8-11ec-98fc-038f439375a0")
result_message_link = gui.get_message_link("fix01:first:1600854429908302153")
print(result_event_link, result_message_link)
