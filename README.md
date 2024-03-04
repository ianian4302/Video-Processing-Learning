# Video-Processing-Learning
A progject of Video-Processing-Learning. 

Programing with Opencv and Python. 

- [Video-Processing-Learning](#video-processing-learning)
- [Detail](#detail)
    - [HW1](#hw1)
        - [Adjusting Wavelengths in the Rotated Rainbow](#adjusting-wavelengths-in-the-rotated-rainbow)
        - [Adjusting Parameters of the Stockman and Sharpe Model](#adjusting-parameters-of-the-stockman-and-sharpe-model)
        - [Adjusting Parameters of the Camera Projection Model](#adjusting-parameters-of-the-camera-projection-model)
    - [HW2](#hw2)
        - [FPS-(Frames Per Second)](fps-(frames-per-second))
        - [Image Height](image-height)
        - [Retrace Times](retrace-times)
#    Detail
#    HW1
##    Adjusting Wavelengths in the Rotated Rainbow

By adjusting the wavelengths of lights in the rotated rainbow experiment, you can observe changes in color perception. Different wavelengths correspond to different colors in the visible spectrum. Red light typically has longer wavelengths, while blue light has shorter wavelengths.

##    Adjusting Parameters of the Stockman and Sharpe Model

The Stockman and Sharpe model is widely used to characterize human color perception. It is based on the sensitivity of three types of cone cells in the retina: short-wavelength (S-cones), medium-wavelength (M-cones), and long-wavelength (L-cones). These cones respond differently to various wavelengths of light.

By adjusting the parameters of this model, such as the spectral sensitivity curves of the cones or the weighting factors applied to different wavelengths, you can simulate different color vision deficiencies (e.g., protanopia, deuteranopia, tritanopia). This analysis can provide insights into how individuals with color vision deficiencies perceive colors differently from those with normal color vision.

##    Adjusting Parameters of the Camera Projection Model
The camera projection model describes how light entering the camera lens is translated into an image. Adjusting parameters such as exposure settings (e.g., aperture, shutter speed, ISO), white balance, and color profile can significantly impact the resulting image.

By analyzing differences in results based on adjustments to these parameters, you can understand how they affect color accuracy, contrast, and overall image quality. This analysis is essential for photographers, videographers, and imaging professionals to produce desired visual outcomes and ensure consistency across different imaging devices.
#    HW2
##    FPS (Frames Per Second)
Higher FPS results in shorter time intervals between frames. This means that the time allocated for each frame (T_frame_ms) decreases, potentially affecting the timing of vertical retrace and completing a full raster scan.
Higher FPS also means more frames to scan within a given time frame, which could increase the workload and affect the timing of horizontal retrace.

##    Image Height
Increasing image height increases the number of lines to be scanned in each frame. This affects the time required for vertical retrace, as well as the total time required to complete a full raster scan.
It also affects the workload during horizontal retrace, as more lines need to be scanned.

##    Retrace Times
Adjusting retrace times directly impacts the timing of horizontal and vertical retraces. Shorter retrace times would mean less time spent on retrace and more time available for actual scanning.
Longer retrace times might result in more noticeable flicker or lag in the display but could also provide more time for other processing tasks.
