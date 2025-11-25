# TODO

- rassembler les fichiers !
- redmine ???

# QML Book

https://www.qt.io/product/qt6/qml-book
**lien cassé !!!**

https://github.com/qmlbook/qt6book
Copyright 2012-2021 Johan Thelin and Jürgen Bocklage-Ryannel

Fixes for `digital envelope routines::unsupported`
```
    "docs:dev": "NODE_OPTIONS=--openssl-legacy-provider vuepress dev docs --host 127.0.0.1",
    "docs:build": "NODE_OPTIONS=--openssl-legacy-provider vuepress build docs",
    "docs:pdf": "NODE_OPTIONS=--openssl-legacy-provider vuepress export docs",
```

`docs/.vuepress/dist` is broken
To fix href
```
cp -r docs/.vuepress/dist .

pushd dist

FIX='s/\/assets/..\/assets/g;s/href="\//href="..\//g'

for i in ch*; do
    pushd $i
    find . -name '*html' -exec sed -i -e $FIX {} \;
    popd
done

FIX='s/assets/assets/g;s/href="\//href="/g'
sed -i -e $FIX index.html

popd
```

# Qt Doc which not so clear

- [Structure of a QML Document | Qt Qml | Qt 6.10.1](https://doc.qt.io/qt-6/qtqml-documents-structure.html)
  pragma
  
# QML questions

- property scope
 [Scope and Naming Resolution | Qt Qml | Qt 6.10.1](https://doc.qt.io/qt-6/qtqml-documents-scope.html)
 QML doesn't require `this`
 
 # QQmlEngine
 
 Each QML component is instantiated in a `QQmlContext`. In QML, contexts are arranged hierarchically
 and this hierarchy is managed by the `QQmlEngine`. By default, components are instantiated in the
 **root context**.
  
 `QQmlContext *QQmlEngine::contextForObject(const QObject *object)`
 `QQmlContext *qmlContext(const QObject *object)`
  
`QObject *QQmlContext::contextObject() const`
  
 `QQmlContext *QQmlContext::parentContext() const`
 
 `void QQmlContext::setContextProperty(const QString &name, QObject *value)`
 `void QQmlContext::setContextProperty(const QString &name, const QVariant &value)`
  `QVariant QQmlContext::contextProperty(const QString &name) const`
  this method does traverse the context hierarchy and searches in parent contexts if the name is not
 found in the current one
 
 `QString QQmlContext::nameForObject(const QObject *object) const`
 `QObject *QQmlContext::objectForName(const QString &name) const`
 
 > You should not use context objects to inject values into your QML components. Use singletons or
 > regular object properties instead.
 
 > You should not use context properties to inject values into your QML components. Use singletons
 > or regular object properties instead.
 
[Exposing State from C++ to QML | Qt Qml | Qt 6.10.1](https://doc.qt.io/qt-6/qtqml-cppintegration-exposecppstate.html)
