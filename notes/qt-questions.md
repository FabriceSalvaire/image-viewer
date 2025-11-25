# QML Flickable

- It seems designed for touch screen...
- Key doesn't work ???
- scrollbar uses percent positioning

# Pad Wheel

- angle is << 120
- angle is not filtered
  flows is - + - - + -...

https://gitlab.gnome.org/GNOME/gtk/-/issues/3631
Touchpad scrolling is too fast-sensitive 

# Action / Shortcut

- https://doc.qt.io/qt-6/qml-qtquick-shortcut.html
  enabled
- https://doc.qt.io/qt-6/qml-qtquick-controls-action.html
  Action represents an abstract user interface action that can have shortcuts and can be assigned to menu items and toolbar buttons.

  https://doc.qt.io/qt-6/qml-qtquick-wheelhandler.html
  
  https://stackoverflow.com/questions/12192780/assigning-keyboard-shortcuts-to-qml-components
  https://doc.qt.io/qt-6/qtqml-javascript-dynamicobjectcreation.html
  
  https://doc.qt.io/qt-6/qshortcut.html
  https://doc.qt.io/qt-6/qtwidgets-widgets-shortcuteditor-example.html
  
```
void QQuickShortcut::grabShortcut(Shortcut &shortcut, Qt::ShortcutContext context)
{
    if (m_completed && !shortcut.keySequence.isEmpty()) {

        QGuiApplicationPrivate *pApp = QGuiApplicationPrivate::instance();
        shortcut.id = pApp->shortcutMap.addShortcut(this, shortcut.keySequence, context, *ctxMatcher());

        if (!m_enabled)
            pApp->shortcutMap.setShortcutEnabled(false, shortcut.id, this);
        if (!m_autorepeat)
            pApp->shortcutMap.setShortcutAutoRepeat(false, shortcut.id, this);
    }
}
```

Application has mode defined by a tree /mode1/mode11/mode111
cf. Emacs
  - global keymap
  - Each major or minor mode can have its own keymap which overrides the global definitions of some keys
  Set mode (major, minor...) -> merge global with modes
  https://www.gnu.org/software/emacs/manual/html_node/emacs/Keymaps.html
  https://www.gnu.org/software/emacs/manual/html_node/elisp/Keymaps.html
  (keymap-global-set "C-x C-b" 'buffer-menu)
  (keymap-set texinfo-mode-map "C-c C-c g" 'texinfo-insert-@group)
QGuiApplication routes key to shortcut map
callback routes ???
- JS or C++/py
- if ?
- function pointer ?
  `var callback = function()`
- signal ?

