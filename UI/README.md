# Pratibimb UI - True Reflection of Digital World

A modern, accessible React application for converting YouTube videos into Braille-ready transcripts for visually impaired users.

## Features

- **Dual Input Methods**: YouTube URL input or video file drag-and-drop
- **Accessibility First**: Designed with WCAG guidelines in mind
- **Real-time Processing**: Live feedback during transcript generation
- **Braille-Ready Output**: AI-enhanced transcripts optimized for Braille conversion
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Modern UI**: Clean, intuitive interface with smooth animations

## Tech Stack

- **React 18** - Modern React with hooks
- **Lucide React** - Beautiful, accessible icons
- **React Dropzone** - Drag and drop file upload
- **Axios** - HTTP client for API communication
- **CSS3** - Modern styling with flexbox and grid

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Running API server (see ../API folder)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Project Structure

```
src/
├── components/
│   ├── Header.js/css         # Application header
│   ├── Footer.js/css         # Application footer
│   ├── YouTubeInput.js/css   # YouTube URL input form
│   ├── FileUpload.js/css     # Drag & drop file upload
│   ├── LoadingSpinner.js/css # Loading indicator
│   └── Results.js/css        # Results display
├── App.js/css               # Main application component
├── index.js                 # React DOM rendering
└── index.css               # Global styles
```

## API Integration

The UI communicates with the FastAPI backend running on `http://localhost:8000`. Ensure the API server is running before using the application.

### Endpoints Used:
- `POST /process_transcript` - Process YouTube URL and return enhanced transcript

## Accessibility Features

- **Keyboard Navigation**: Full keyboard support
- **Screen Reader Compatible**: Proper ARIA labels and semantic HTML
- **High Contrast Support**: Adapts to user's contrast preferences
- **Reduced Motion Support**: Respects user's motion preferences
- **Focus Management**: Clear focus indicators and logical tab order

## Design Philosophy

The UI follows the principle of "True Reflection of Digital World" by:

1. **Inclusivity**: Making digital content accessible to everyone
2. **Simplicity**: Clean, distraction-free interface
3. **Efficiency**: Streamlined workflow from input to output
4. **Reliability**: Robust error handling and user feedback

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow React best practices
2. Maintain accessibility standards
3. Write semantic HTML
4. Test on multiple devices and screen readers
5. Follow the existing code style

## License

This project is part of the Pratibimb accessibility initiative.
