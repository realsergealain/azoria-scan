import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from io import BytesIO
from PIL import Image

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (0, 0, 0)

def generate_styled_qr_code(data: str, color_hex: str = '#7C3AED', logo_path: str = None) -> BytesIO:
    """
    Génère un QR Code stylisé premium avec des coins arrondis et une couleur personnalisée.
    """
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    rgb_color = hex_to_rgb(color_hex)

    # Style: Coins arrondis et couleur personnalisée
    img_factory = StyledPilImage
    img_args = {
        'module_drawer': RoundedModuleDrawer(),
        'color_mask': SolidFillColorMask(back_color=(255, 255, 255), front_color=rgb_color)
    }

    if logo_path:
        try:
            # We would need a mechanism to pass the image stream or path
            # For this MVP, we will just use the color mask if logo is too complex to load dynamically
            pass
        except Exception:
            pass

    img = qr.make_image(image_factory=img_factory, **img_args)
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
