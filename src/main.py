import threading
from processes import RunArtefact, TrafficCapture
import RPi.GPIO as GPIO


def main():
    traffic_capture = TrafficCapture()
    run_artefact = RunArtefact(traffic_capture)
    traffic_capturing_process = threading.Thread(target=traffic_capture.capture_data_traffic)
    artefact_running_process = threading.Thread(target=run_artefact.between_callback)
    try:
        traffic_capturing_process.start()
        artefact_running_process.start()
    except KeyboardInterrupt:
        traffic_capturing_process.join()
        artefact_running_process.join()
        GPIO.clean_up()


if __name__ == "__main__":
    main()
