from pathlib import Path
import ipywidgets as ipw


class NotePlayer(ipw.VBox):
    """
    Display a sequence of images with a widget player control.
    
    Parameters
    ----------
    
    folder : str
        Path to folder with images. All images in this folder will be displayed,
        in whatever order ``sorted`` leads to.
        
    description : str, optional
        Title above the player.
        
    width : str, optional
        Width of the display. Can be in pixels, e.g. '300px' or any other valid CSS
        expression for width, e.g. '100%'. 
        
    interval : int, optional
        Delay between images, in milliseconds.
        
    Attributes
    ----------
    
    html :
        The `ipywidgets.HTML` title/description above the player.
        
    image :
        The `ipywidgets.Image` widget that displays the images.
        
    play :
        The `ipywidgets.Play` widget that controls playback.
    """
    def __init__(self, folder, *args, 
                 description=None, width='400px', interval=1000,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.imgs = []
        self.folder = folder
        self.html = ipw.HTML(value=description)
        self.image = ipw.Image()
        self.image.layout = ipw.Layout(width=width)
        
        self._init_image_paths()
        self.play = ipw.Play(interval=interval, max=len(self.imgs) - 1)
        self.play.layout = self.image.layout

        self._set_observers()
        
        self.children = (self.html, self.play, self.image)
        self.set_image(0)
        
    def _init_image_paths(self):
        im_folder = Path(self.folder)
        self.imgs = sorted(im_folder.glob('*.jpg'))
        
    def set_image(self, num):
        """
        Set image to particular index.
        
        Parameters
        ----------
        
        num : int
            Index of the image to display in ``self.imgs``.
        """
        with open(self.imgs[num], 'rb') as f:
            im_content = f.read()
        self.image.value = im_content
        
    def _set_observers(self):
        def play_display_image(change):
            im_num = change['new'] 
            self.set_image(im_num)
            
        self.play.observe(play_display_image, names=['value'])