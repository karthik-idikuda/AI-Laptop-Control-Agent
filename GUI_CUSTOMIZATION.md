# OS Agent GUI - macOS Customization Guide

## 🎨 Current macOS Settings

### Window Position
- **Location**: Top-right corner
- **Spacing**: 20px from edges (respects macOS menu bar)
- **Size**: 360x500px (compact for side placement)

### Window Behavior
- ✅ **Always on top** - Won't hide behind other windows
- ✅ **Frameless** - Clean, minimal design
- ✅ **Draggable** - Click and drag anywhere to move
- ✅ **95% opacity** - Slight transparency (macOS style)

### macOS-Native Features
- 🎨 **Helvetica Neue** font throughout
- 🎨 **Monaco** monospace for logs
- 🎨 **Slate color palette** (modern dark theme)
- 🎨 **Glassmorphism** effects

## 🛠️ Customization Options

### Change Position
Edit `gui_advanced.py`, line 46-50:

```python
# Top-right (current)
x = screen.width() - w - 20
y = 20

# Top-left
x = 20
y = 20

# Bottom-right
x = screen.width() - w - 20
y = screen.height() - h - 40

# Bottom-left
x = 20
y = screen.height() - h - 40
```

### Adjust Opacity
Edit `gui_advanced.py`, line 56:

```python
# Current (95% visible)
self.setWindowOpacity(0.95)

# Fully opaque
self.setWindowOpacity(1.0)

# More transparent (80%)
self.setWindowOpacity(0.8)
```

### Change Size
Edit `gui_advanced.py`, line 48:

```python
# Current
w, h = 360, 500

# Wider
w, h = 450, 500

# Taller
w, h = 360, 650

# Compact
w, h = 300, 400
```

### Disable Always-on-Top
Edit `gui_advanced.py`, line 54:

```python
# Current (always on top)
self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

# Normal behavior
self.setWindowFlags(Qt.FramelessWindowHint)
```

## 🎯 macOS Integration Tips

### Mission Control
The GUI will:
- ✅ Show in all Spaces (due to always-on-top)
- ✅ Appear in Mission Control
- ✅ Stay visible during Space switching

### Hot Corners
Position chosen to avoid triggering:
- Top-right hot corner (if you have one set)
- Uses 20px margin to prevent PyAutoGUI failsafe

### Menu Bar
- 20px top margin ensures it doesn't overlap menu bar
- Respects macOS menu bar height automatically

## 🔧 Advanced Customization

### Add Window Title Bar (macOS-style)
Remove frameless flag:

```python
# Standard macOS window with traffic lights
self.setWindowFlags(Qt.WindowStaysOnTopHint)
# Remove: Qt.FramelessWindowHint
```

### Make it Resizable
Remove fixed width:

```python
# Comment out:
# self.setFixedWidth(w)
```

### Add to Dock
The app already appears in Dock when running. To make it permanent, create an .app bundle.

## 📍 Current Layout

```
┌────────────────────────────────────────────┐
│  macOS Menu Bar                            │
│                                    ┌──────┐│ <- 20px margin
│                                    │      ││
│                                    │ OS   ││
│                                    │Agent ││
│                                    │ Pro  ││
│                                    │      ││
│                                    │      ││
│                                    │      ││
│                                    └──────┘│ <- 20px margin
└────────────────────────────────────────────┘
```

## 🎨 Color Customization

All colors use Tailwind CSS Slate palette. To change:

Edit `gui_advanced.py`, search for color codes:

- Background: `#0f172a` (Slate 900)
- Border: `#334155` (Slate 700)
- Text: `#f8fafc` (Slate 50)
- Accent: `#3b82f6` (Blue 500)

## ✅ Applied Settings

- [x] Top-right corner positioning
- [x] Always on top
- [x] 95% opacity
- [x] Draggable
- [x] Frameless window
- [x] macOS-native fonts
- [x] 20px margins
- [x] Respects menu bar

Restart the GUI to see changes!
