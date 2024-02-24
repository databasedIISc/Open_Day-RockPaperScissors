import cv2
import time
import random
import keyboard
import HandTrackingModule as htm


def rps():
    cap = cv2.VideoCapture(0)
    wCam, hCam = 1920, 1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)

    detector = htm.handDetector(detectionCon=0.5, maxHands=1, trackCon=0.8)

    ready = True
    computer = ["Rock", "Paper", "Scissors"]
    score = 0
    round = 1
    timer = time.time()
    enter = time.time()
    enter_start = True
    round_next = False
    time_start = False

    while True:
        success, img = cap.read()
        
        img_flipped = cv2.flip(img, 1)
        img_flipped_cropped = img_flipped[0:873, 0:1460]
        img = detector.findHands(img_flipped_cropped)
        

        lmList0, box0 = detector.findPosition(img, handNo=0, draw_circle=True, draw_box=False)
        
        if round == 0:
            detector.findPosition(img, handNo=1, draw_circle=True, draw_box=False)
            detector.findPosition(img, handNo=2, draw_circle=True, draw_box=False)
            detector.findPosition(img, handNo=3, draw_circle=True, draw_box=False)

        fingers = []
        player = ""

        if keyboard.is_pressed("esc"):
            round = 0
            detector.is_game = False
        if keyboard.is_pressed("enter"):
            round = 1
            score = 0
            detector.is_game = True

        if len(lmList0) == 0:
            enter_start = True

        if len(lmList0) != 0:
            area0 = (box0[2] - box0[0]) * (box0[3] - box0[1]) // 100
            cv2.putText(img, f"Hand detected", (30, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            if area0 > 200:
                if enter_start:
                    enter = time.time()
                    enter_start = False
                if enter + 0.5 < time.time():
                    fingers = detector.fingersUp(lmList0)

        if len(fingers) == 0:
            if time_start:
                timer = time.time()
                time_start = False
            if timer + 1 < time.time():
                ready = True
                if 0 < round <= 5 and round_next:
                    round += 1
                    round_next = False
                    
        if 0 < round <= 5:    
            if fingers[1:] == [0]*4 and ready:
                player = "Rock"

            if fingers == [1]*5 and ready:
                player = "Paper"

            if fingers == [0,1,1,0,0] and ready:
                player = "Scissors"

            if len(player) != 0:
                player_copy = player
                ready = False
                round_next = True
                time_start = True
                computer_choice = random.choice(computer)

                if player == computer_choice:
                    score += 1
                elif player == "Rock" and computer_choice == "Scissors":
                    score += 3
                elif player == "Rock" and computer_choice == "Paper":
                    score += 0
                elif player == "Paper" and computer_choice == "Rock":
                    score += 3
                elif player == "Paper" and computer_choice == "Scissors":
                    score += 0
                elif player == "Scissors" and computer_choice == "Paper":
                    score += 3
                elif player == "Scissors" and computer_choice == "Rock":
                    score += 0

            cv2.putText(img, "Score: {0}".format(score), (30,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
            cv2.putText(img, "Round: {0}/5".format(round), (1050,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

            if ready:
                cv2.putText(img, "Ready!", (550,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            else:
                cv2.putText(img, "You: {0}".format(player_copy), (30,350), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
                cv2.putText(img, "Computer: {0}".format(computer_choice), (30,400), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)


        elif round > 5:
            cv2.putText(img, "Score: {0}".format(score), (550,400), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
            if score >= 8:
                cv2.putText(img, "You Win!", (550,450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
            else:
                cv2.putText(img, "You Lose!", (550,450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

        cv2.imshow("Image", img_flipped)
        cv2.waitKey(1)

rps()
