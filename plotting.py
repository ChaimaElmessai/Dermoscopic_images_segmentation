def plot_steps(steps):
  fig, axs = plt.subplots(2, 3,figsize=(15,8))
  axs[0][0].imshow(original_image);
  axs[0][0].set_title('Original Image');
  axs[0][1].imshow(filtered_image,cmap='gray');
  axs[0][1].set_title('Filtered Image');
  axs[0][2].imshow(adjusted_image,cmap='gray');
  axs[0][2].set_title('Image Intensity Adjustement');
  axs[1][0].imshow(th_image,cmap='gray');
  axs[1][0].set_title('Thresholding');
  axs[1][1].imshow(cca_image,cmap='gray');
  axs[1][1].set_title('Connected Components');
  axs[1][2].imshow(1- dilated,cmap='gray');
  axs[1][2].set_title('Filled Image');
  plt.show()