import cv2

# Load the image
foto = "himne_alegria_full.png"
img = cv2.imread('sheets/' + foto)

# Resize the image
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

# Create a list to store the points
points = []

# Define the event callback function


def click_event(event, x, y, flags, param):
    # Check if left mouse button is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append the clicked point to the list
        points.append((int(x*2), int(y*2)))
        # Display the point on the image
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('image', img)


# Display the image
cv2.imshow('image', img)

# Set the mouse callback function
cv2.setMouseCallback('image', click_event)

# Wait for the user to select points
cv2.waitKey(0)

# Save the points to a txt file
with open('sheets/points_' + foto + '.txt', 'w') as file:
    for point in points:
        file.write(f'{point[0]},{point[1]}\n')

# Close all windows
cv2.destroyAllWindows()
