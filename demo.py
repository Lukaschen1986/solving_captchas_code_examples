pic = Image.open("3385254739.png", mode="r")
pic_array = image.img_to_array(pic, "channels_last").astype("uint8") # img_to_array
pic_grey = cv2.cvtColor(pic_array, code=cv2.COLOR_BGR2GRAY)
pic_grey_2 = cv2.copyMakeBorder(pic_grey, top=20, bottom=20, left=20, right=20, borderType=cv2.BORDER_REPLICATE)
pic_grey_3 = cv2.threshold(pic_grey_2, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)[1] # 二值化 与 黑白翻转
contours = cv2.findContours(pic_grey_3.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

contours = contours[1]

letter_image_regions = []
for contour in contours:
    # contour = contours[1]
    # Get the rectangle that contains the contour
    (x, y, w, h) = cv2.boundingRect(contour)

    # Compare the width and height of the contour to detect letters that
    # are conjoined into one chunk
    if w / h > 0.75:
        # This contour is too wide to be a single letter!
        # Split it in half into two letter regions!
        half_width = int(w / 2)
        letter_image_regions.append((x, y, half_width, h))
        letter_image_regions.append((x + half_width, y, half_width, h))
    else:
        # This is a normal letter by itself
        letter_image_regions.append((x, y, w, h))

# with the right letter
letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])
        
for letter_bounding_box in letter_image_regions:
    letter_bounding_box = letter_image_regions[0]
    x, y, w, h = letter_bounding_box
    letter_pic = pic_grey_3[y - 2:y + h + 2, x - 2:x + w + 2]
