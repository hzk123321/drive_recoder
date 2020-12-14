import shutil
import cv2
import os
import datetime
 
camera = cv2.VideoCapture(0)                               # カメラCh.(ここでは0)を指定
 
# 動画ファイル保存用の設定
fps = int(camera.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得

print(fps)
 
while True:
    dt_now = datetime.datetime.now()

    # 古い動画の削除
    yesterday = dt_now - datetime.timedelta(days=1)
    try:
        shutil.rmtree(yesterday.strftime('%Y%m%d'))
    except OSError as e:
        print("NONONO")    

    folder_name = dt_now.strftime('%Y%m%d')
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    video_name = folder_name + "/" + dt_now.strftime('%Y%m%d%H%M%S') + ".mp4"
    print(video_name)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
    video = cv2.VideoWriter(video_name, fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

    count = 0

# 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
    while True:
        ret, frame = camera.read()                             # フレームを取得
        cv2.imshow('camera', frame)                            # フレームを画面に表示
        video.write(frame)                                     # 動画を1フレームずつ保存する
 
        count = count + 1
        if count == (fps * 5):
            break;

        # キー操作があればwhileループを抜けて終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
# 撮影用オブジェクトとウィンドウの解放
            camera.release()
            cv2.destroyAllWindows()
            exit()
