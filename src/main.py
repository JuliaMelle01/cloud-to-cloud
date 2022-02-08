import threading
from processes import RunArtefact, TrafficCapture
import RPi.GPIO as GPIO


def main():
    """
    main function to be called when starting cloud-to-cloud artefact
    software. Calling the function start two ongoing processes on two
    threads. One is for capturing piped into data traffic and the other
    one is for updating the state of the artefact accordingly.
    """
    # Ongoing process of data traffic capturing
    traffic_capture = TrafficCapture()
    # Hourly process updating status artefact
    run_artefact = RunArtefact(traffic_capture)
    # Assign processes to threads
    traffic_capturing_process = threading.Thread(
        target=traffic_capture.capture_data_traffic
    )
    artefact_running_process = threading.Thread(target=run_artefact.between_callback)
    try:
        # start processes
        traffic_capturing_process.start()
        artefact_running_process.start()
    except KeyboardInterrupt:
        # Keyboard interrupt stops the processes
        # and ends the connection to the GPIO pins
        traffic_capturing_process.join()
        artefact_running_process.join()
        GPIO.clean_up()


if __name__ == "__main__":
    main()
