import os
import azure.ai.vision as sdk
import cv2 as cv
import tkinter as tk

service_options = sdk.VisionServiceOptions(os.environ["VISION_ENDPOINT"],
                                           os.environ["VISION_KEY"])

cam_port = 0
cam = cv.VideoCapture(cam_port)

result, image = cam.read()
file_path = "Pictures\image.png"

if result:
    cv.imshow("image", image)
    cv.imwrite("Pictures\image.png", image)
    cv.waitKey(0)
    cv.destroyWindow("image")
    vision_source = sdk.VisionSource(file_path)

    analysis_options = sdk.ImageAnalysisOptions()

    analysis_options.features = (
    sdk.ImageAnalysisFeature.CAPTION |
    sdk.ImageAnalysisFeature.TEXT
    )

    analysis_options.language = "en"

    analysis_options.gender_neutral_caption = True

    image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

    result = image_analyzer.analyze()

    if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:

        if result.caption is not None:
            print(" Caption:")
            print("   '{}', Confidence {:.4f}".format(result.caption.content, result.caption.confidence))

        if result.text is not None:
            print(" Text:")
            for line in result.text.lines:
                points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
                print("   Line: '{}', Bounding polygon {}".format(line.content, points_string))
                for word in line.words:
                    points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                    print("     Word: '{}', Bounding polygon {}, Confidence {:.4f}"
                          .format(word.content, points_string, word.confidence))

    else:

        error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
        print(" Analysis failed.")
        print("   Error reason: {}".format(error_details.reason))
        print("   Error code: {}".format(error_details.error_code))
        print("   Error message: {}".format(error_details.message))
else:
    print("No image detected. Please! try again")