from PyQt5.QtWidgets import QLineEdit, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QWidget, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt, QTimer
import subprocess, re

class DDC_Control(QWidget):

    def __init__(self):

        super().__init__()
        self.initUI()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)  # Only trigger once after timer
        self.timer.timeout.connect(self.apply_brightness)

        self.monitors = self.auto_detect_monitors()
        
        self.create_autodetect_checkbox()
        self.create_dynamic_inputs()
        self.create_buttons("help")
        self.create_dynamic_sliders()
        self.create_buttons("apply")

        self.toggle_bus_input_fields()


    def initUI(self):

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("DDC_Control")

    def create_autodetect_checkbox(self):

        self.autodetect_checkbox = QCheckBox("Autodetect Bus Numbers")
        self.autodetect_checkbox.setChecked(True)
        self.autodetect_checkbox.stateChanged.connect(self.toggle_bus_input_fields)
        self.layout.addWidget(self.autodetect_checkbox)

    def toggle_bus_input_fields(self):

        # Enable or disable the bus input fields based on checkbox state
        autodetect = self.autodetect_checkbox.isChecked()

        for index, _ in enumerate(self.monitors):

            bus_input = getattr(self, f"bus_input{index + 1}")
            bus_input.setEnabled(not autodetect)

    def create_dynamic_inputs(self):

        for i, bus_number in enumerate(self.monitors):

            # Create Bus Number input field for each monitor
            bus_layout = QHBoxLayout()
            bus_label = QLabel(f"Enter Bus Number for Monitor {i + 1}:")
            bus_input = QLineEdit()
            bus_input.setText(str(bus_number))  # Default to detected bus number
            bus_layout.addWidget(bus_label)
            bus_layout.addWidget(bus_input)
            self.layout.addLayout(bus_layout)

            setattr(self, f"bus_input{i + 1}", bus_input)

    def create_dynamic_sliders(self):

        for i, bus_number in enumerate(self.monitors):

            # Create Brightness slider for each monitor
            
            brightness = self.get_brightness(bus_number)

            hbox = QHBoxLayout()
            label = QLabel(f"Brightness {i + 1}:")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(brightness)
            perc_label = QLabel(str(brightness))
            hbox.addWidget(label)
            hbox.addWidget(slider)
            hbox.addWidget(perc_label)

            self.layout.addLayout(hbox)

            setattr(self, f"slider{i + 1}", slider)

            # using slider starts timer so that commands are only run after adjustment is finished
            slider.valueChanged.connect(lambda: self.start_timer())  
            slider.valueChanged.connect(lambda value, lbl=perc_label: lbl.setText(f"{value}%"))         

    def create_buttons(self, name):

        if name == "help":

            help_button = QPushButton("Help")
            help_button.clicked.connect(self.show_help)
            self.layout.addWidget(help_button)

        elif name == "apply":

            apply_button = QPushButton("Force Apply")
            apply_button.clicked.connect(self.apply_brightness)
            self.layout.addWidget(apply_button)
        
    def start_timer(self):

        self.timer.start(250)

    def apply_brightness(self):

        for i, bus_number in enumerate(self.monitors):

            bus_input = getattr(self, f"bus_input{i + 1}").text().strip()
            slider_value = getattr(self, f"slider{i + 1}").value()

            bus_number = bus_input if not self.autodetect_checkbox.isChecked() else str(bus_number)

            if not bus_input.isdigit():

                print(f"Error: Please enter a valid bus number for monitor {i + 1}.")
                continue

            command = f"ddcutil --bus={bus_number} setvcp 10 {slider_value}"

            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error applying brightness to monitor {i + 1}: {e}")

    def get_brightness(self, bus):

        command = f"ddcutil --bus={bus} getvcp 10"
        
        try:
            output = subprocess.check_output(command, shell=True, text=True)     
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        found = re.search(r"current value\s*=\s*(\d+)", output)
        if found:
            return int(found.group(1)) 
        else:
            return null  


    def auto_detect_monitors(self):      

        command = "ddcutil detect | grep bus"

        try:
            output = subprocess.check_output(command, shell=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")    

        bus_numbers = []
        lines = output.splitlines()

        for x in lines:

            bus_numbers.append(int(x[-1]))


        return bus_numbers

    def show_help(self):

        help_message = (
            "To find the correct bus numbers for your monitors run this command:\n\n"
            "ddcutil detect | grep bus\n\n"
            "It's the number on the end of the outputs.\n\n"
            "Example:\n\n"
            "I2C bus:  /dev/i2c-5   ->  5\n"
            "I2C bus:  /dev/i2c-6   ->  6"
        )
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Help")
        msg_box.setText(help_message)
        msg_box.exec_()

if __name__ == "__main__":

    app = QApplication([])
    window = DDC_Control()
    window.show()
    app.exec_()
