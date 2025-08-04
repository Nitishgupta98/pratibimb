# Dhvani Assistant - Component Specification

## Overview
The Dhvani Assistant is an AI-powered voice assistant for accessibility content delivery and device management. It features multiple tabs for managing audiobooks, devices, and content distribution with a focus on school administration and student device management.

## Visual Structure from Screenshot and HTML Analysis

### Header Section
- **Title**: "🎙️ Dhvani Assistant" (with microphone emoji)
- **Subtitle**: "AI-powered voice assistant for accessibility content delivery and device management"
- **Header styling**: Purple theme consistent with application design (#7b2cbf)

### Tab Navigation
Four main tabs in horizontal layout:

1. **📚 Open Source Audiobooks** (Active tab in screenshot)
   - Icon: Book/library icon
   - Text: "Open Source Audiobooks"
   - Purple background when active

2. **📁 Local Audio Files**
   - Icon: Folder icon
   - Text: "Local Audio Files"

3. **Device Management**
   - Icon: Mobile/device icon
   - Text: "Device Management"

4. **☁️ Content Push**
   - Icon: Cloud/share icon
   - Text: "Content Push"

### Main Content Area - Open Source Audiobooks Section

#### Audiobook Grid Layout
Six audiobook cards arranged in a 2x3 grid:

**Row 1:**
1. **The Great Gatsby**
   - Author: F. Scott Fitzgerald
   - Duration: 4h 32m
   - Purple book icon
   - Purple "Play" button

2. **Pride and Prejudice**
   - Author: Jane Austen  
   - Duration: 11h 5m
   - Purple book icon
   - Purple "Play" button

3. **Alice's Adventures in Wonderland**
   - Author: Lewis Carroll
   - Duration: 2h 45m
   - Blue book icon
   - Purple "Play" button

**Row 2:**
4. **The Adventures of Sherlock Holmes**
   - Author: Arthur Conan Doyle
   - Duration: 8h 20m
   - Red book icon
   - Purple "Play" button

5. **Frankenstein**
   - Author: Mary Shelley
   - Duration: 6h 15m
   - Green book icon
   - Purple "Play" button

6. **The Time Machine**
   - Author: H.G. Wells
   - Duration: 3h 12m
   - Orange book icon
   - Purple "Play" button

### Local Audio Files Tab Content
- **Section Header**: "📚 Local Audio Files & Transcripts"
- **Description**: "Available content for distribution to student devices"
- **Grid Layout**: Similar audiobook cards for local files
- **Add to Cart functionality**: Each card has "Add to Cart" button

### Device Management Tab Content
- **Section Header**: "📱 Device Management"
- **Description**: "Manage Dhvani devices and student assignments"
- **Device Cards**: Grid layout showing device information
- **Device Card Content**:
  - Device ID (e.g., "Dhvani Device #001")
  - Model information (e.g., "DH-Pro-2024")
  - Status: "Assigned" or "Unassigned"
  - Student information (if assigned):
    - Name, Age, Grade, Language, School, Device Age
  - Action buttons: "Push Content", "Reassign" for assigned devices
  - "Assign Device" button for unassigned devices

### Content Push Tab Content
- **Content Cart Section**:
  - Cart header with item count
  - "Clear Cart" button
  - List of selected content items
  - Remove buttons for each item

- **Push Target Selection**:
  - Radio buttons for target selection:
    - "Push to all students in school"
    - "Push to selected students"
  - Student selector (when "selected students" is chosen)
  - Checkboxes for individual student selection

- **Push Button**: Main action button to distribute content

### Role-Based Access Control
- **School Admin Role**: Full access to all features
- **Teacher Role**: Limited access (specific tabs may be hidden)
- **Device assignment modal** for assigning devices to students

## Technical Features

### Interactive Elements
1. **Tab Switching**: Active tab highlighting with smooth transitions
2. **Audio Playback**: Play buttons for audiobook preview
3. **Cart Management**: Add/remove items, cart counter
4. **Device Assignment**: Modal dialog for student assignment
5. **Content Distribution**: Bulk push to devices
6. **Student Selection**: Multi-select checkboxes
7. **Responsive Design**: Mobile-friendly layout

### State Management Required
- Active tab tracking
- Cart contents and count
- Selected students for content push
- Device assignment modal state
- Role-based UI visibility
- Success/error message display

### Data Structures

#### Audiobook Object
```javascript
{
  id: string,
  title: string,
  author: string,
  duration: string,
  cover: string (emoji or icon),
  type: 'audio' | 'transcript',
  source: 'opensource' | 'local'
}
```

#### Device Object
```javascript
{
  id: string,
  model: string,
  status: 'assigned' | 'unassigned',
  student?: {
    name: string,
    age: number,
    grade: string,
    language: string,
    school: string,
    deviceAge: string
  }
}
```

#### Student Object
```javascript
{
  id: number,
  name: string,
  grade: string,
  device: string | null
}
```

## Design Specifications

### Color Scheme
- **Primary Purple**: #7b2cbf (consistent with app theme)
- **Background**: Light gray (#f8f9fa)
- **Cards**: White background with subtle shadows
- **Buttons**: Purple primary, green success, orange warning
- **Text**: Dark gray (#333) for headings, medium gray (#666) for secondary

### Layout Specifications
- **Container**: Max-width with centered alignment
- **Grid**: Responsive grid for audiobook/device cards
- **Spacing**: Consistent padding and margins
- **Cards**: Rounded corners, hover effects, shadows
- **Typography**: Clear hierarchy with proper font weights

### Animation and Interactions
- **Tab transitions**: Smooth switching between tabs
- **Button hover effects**: Scale and color changes
- **Card hover effects**: Subtle lift and shadow increase
- **Loading states**: For content operations
- **Success/error messages**: Toast notifications

## Component Structure

### Main Component: DhvaniAssistant.js
- Tab management state
- Cart management logic
- Device assignment functionality
- Content push operations
- Role-based rendering

### Sub-components or Sections:
1. **Header section** with title and description
2. **Tab navigation** with active state management
3. **OpenSourceAudiobooks** section
4. **LocalAudioFiles** section
5. **DeviceManagement** section
6. **ContentPush** section
7. **AssignmentModal** for device assignments
8. **MessageToast** for user feedback

## Implementation Requirements

### Dependencies
- React hooks (useState, useEffect)
- Font Awesome icons for UI elements
- CSS Grid/Flexbox for responsive layouts
- Modal dialog functionality
- Local storage for cart persistence

### Accessibility Features
- Proper ARIA labels for screen readers
- Keyboard navigation support
- High contrast color schemes
- Focus management for modals
- Semantic HTML structure

## Sample Data Requirements

### Open Source Audiobooks (6 items)
- Classic literature with varied authors and durations
- Different colored book icons for visual distinction
- Professional duration formatting (hours and minutes)

### Local Audio Files (5 items)
- Educational content for school distribution
- Mix of audio and transcript types
- Add to cart functionality

### Device Information (6 devices)
- Mix of assigned and unassigned devices
- Different device models (Pro, Standard, Lite)
- Student demographic information
- Assignment history and device age

### Student Database (5 students)
- Names, grades, and current device assignments
- Available students for new device assignments
- Multi-select functionality for content distribution

## File Structure
- Component: `DhvaniAssistant.js`
- Styling: `DhvaniAssistant.css`  
- This specification: `DhvaniAssistantReadme.md`

## Notes for Implementation
- Maintain consistency with existing Learning Center components
- Ensure proper state management for cart and selections
- Implement proper error handling and user feedback
- Make it demo-ready with realistic sample data
- Follow the exact visual design from the HTML file and screenshot
