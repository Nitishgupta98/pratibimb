# 🔤 Pratibimb - Enhanced Braille Converter with Art Support

Professional Grade 1 Braille converter with **revolutionary image-to-Braille art conversion** for complete accessibility.

## 🚀 NEW: Braille Art Support (v2.1)

Pratibimb now converts images into tactile Braille graphics, providing blind and visually impaired users with access to visual content through touch.

### ✨ Key Features

**Text Conversion:**
- ✅ Grade 1 Braille (letter-for-letter, no contractions)
- ✅ Unicode Braille output for screen readers  
- ✅ ASCII BRF format for professional embossers
- ✅ 40 chars/line, 25 lines/page formatting
- ✅ Comprehensive validation and testing

**🆕 Image-to-Braille Art:**
- 🖼️ Convert images to tactile Braille patterns
- 📐 Automatic sizing and optimization
- 🎨 Edge enhancement for better tactile definition
- 🔧 Configurable contrast and brightness
- 🌐 Support for local files, URLs, and base64 data
- 📋 Embeds seamlessly in Braille documents

## 🖼️ Using Braille Art

### Image Reference Syntax

Include images in your text using these formats:

```
[IMAGE: path/to/image.jpg]
[IMAGE: path/to/image.jpg | Title]
[IMAGE: path/to/image.jpg | Title | Description]
```

### Examples

**Basic Image:**
```
[IMAGE: logo.png]
```

**Image with Title:**
```
[IMAGE: chart.jpg | Sales Chart]
```

**Image with Full Description:**
```
[IMAGE: diagram.png | Network Diagram | Shows the connection between servers and clients in our system architecture]
```

### Supported Image Sources

1. **Local Files**: `images/photo.jpg`, `../assets/logo.png`
2. **Web URLs**: `https://example.com/image.jpg`
3. **Base64 Data**: `data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAE...`

### Supported Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)

## 📋 Installation

### Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Required packages for Braille Art:
pip install Pillow>=10.0.0 numpy>=1.21.0
```

### Quick Start

1. **Prepare your text file** with image references:
```
Welcome to our organization.

[IMAGE: logo.png | Company Logo]

Our mission is to provide accessibility solutions.

[IMAGE: chart.jpg | Annual Results | Bar chart showing 25% growth]
```

2. **Configure settings** in `config.json`:
```json
{
    "input_file": "examples/input_text_with_images.txt",
    "output_file": "output/braille_output_with_art.txt",
    "embosser_file": "output/embosser_ready_with_art.brf",
    "braille_art_settings": {
        "process_images": true,
        "target_width": 38,
        "target_height": 24,
        "contrast_boost": 1.5,
        "include_border": true
    }
}
```

3. **Run the converter**:
```bash
python pratibimb.py
```

## ⚙️ Braille Art Configuration

### Processing Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `process_images` | `true` | Enable/disable image processing |
| `target_width` | `38` | Width in Braille characters |
| `target_height` | `24` | Height in Braille lines |
| `contrast_boost` | `1.5` | Contrast enhancement factor |
| `brightness_boost` | `1.2` | Brightness adjustment |
| `edge_enhance` | `true` | Enable edge enhancement |
| `threshold` | `128` | Brightness threshold (0-255) |
| `invert_colors` | `false` | Invert black/white |
| `include_border` | `true` | Add border around art |
| `border_char` | `"⠿"` | Character for borders |
| `use_8dot_braille` | `false` | Use 8-dot for higher resolution |

### Advanced Configuration

```json
{
    "braille_art_settings": {
        "process_images": true,
        "target_width": 38,
        "target_height": 24,
        "contrast_boost": 1.8,
        "brightness_boost": 1.3,
        "edge_enhance": true,
        "use_8dot_braille": false,
        "threshold": 120,
        "invert_colors": false,
        "include_border": true,
        "border_char": "⠿"
    }
}
```

## 🔄 Workflow

1. **Text Analysis**: Parse input text for image references
2. **Image Loading**: Fetch images from various sources
3. **Preprocessing**: Resize, enhance contrast, apply filters
4. **Braille Conversion**: Convert pixels to Braille dot patterns
5. **Art Formatting**: Add titles, descriptions, borders
6. **Text Integration**: Embed art seamlessly in Braille text
7. **Output Generation**: Create Unicode and BRF files

## 📊 Output Examples

### Text Output (Unicode Braille)
```
[Image: Company Logo]

⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿
⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿
⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿
⠿⠀⠀⠀⠀⠀⠀⠀⠀⠓⠳⠞⠝⠊⠍⠃⠊⠞⠁⠗⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿
⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿
⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿

Description: The official logo of Pratibimb accessibility platform
```

### BRF Output (ASCII for Embossers)
```
[Image: Company Logo]

???????????????????????????????????????????????????????
?                                      ?
?                                      ?
?        ,pratibimb,                   ?
?                                      ?
???????????????????????????????????????????????????????

Description: The official logo of Pratibimb
accessibility platform
```

## 🧪 Testing

The enhanced testing suite includes Braille art validation:

```bash
python pratibimb.py
```

Tests include:
- ✅ Embosser validation
- ✅ Braille analysis  
- ✅ Batch conversion
- ✅ Round-trip conversion
- 🆕 **Braille art processing**
- ✅ Format compliance

## 🎯 Use Cases

### Educational Materials
- Convert diagrams, charts, and illustrations
- Make textbooks fully accessible
- Provide tactile learning experiences

### Business Documents
- Include logos, charts, and graphics
- Professional reports with visual elements
- Accessible presentations and materials

### Personal Content
- Family photos and memories
- Art and creative content
- Social media images with descriptions

## 🔧 Troubleshooting

### Common Issues

**Image not found:**
```
[Error: Could not load image from path/to/image.jpg]
```
- Check file path and permissions
- Ensure image file exists
- Try absolute path

**Processing errors:**
```
[Error: Could not preprocess image]
```
- Check image format compatibility
- Verify image is not corrupted
- Try reducing image size

**Poor tactile quality:**
- Increase `contrast_boost` (try 2.0)
- Enable `edge_enhance`
- Adjust `threshold` value
- Try `use_8dot_braille: true`

### Performance Tips

- Keep images under 2MB for faster processing
- Use high-contrast images for better results
- Prefer PNG format for logos and diagrams
- Use JPEG for photographs

## 📚 Technical Details

### Braille Dot Patterns

**6-dot Braille Cell:**
```
1 4
2 5  
3 6
```

**8-dot Braille Cell:**
```
1 4
2 5
3 6
7 8
```

### Processing Algorithm

1. **Load** image from source
2. **Convert** to grayscale
3. **Resize** to target dimensions
4. **Enhance** contrast and brightness
5. **Apply** edge detection
6. **Map** pixels to Braille dots
7. **Generate** Unicode patterns
8. **Format** with borders and descriptions

## 🤝 Contributing

We welcome contributions to enhance Braille art capabilities:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

Professional Use License - See LICENSE file for details.

## 📞 Support

For questions about Braille art features:
- 📧 Email: support@pratibimb.com
- 📚 Documentation: [Full Guide](./ui/Documentation.html)
- 🐛 Issues: [GitHub Issues](./issues)

---

**Pratibimb v2.1** - Making visual content accessible through innovative Braille art technology.
