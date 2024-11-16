# Maintainer: Your Name <your.email@example.com>

pkgname=cac-manager
pkgver=1.0.0
pkgrel=1
pkgdesc="Manage DoD Common Access Cards (CAC) on Linux"
arch=('x86_64')
url="https://github.com/large-farva/cac-manager"
license=('MIT')
depends=('python' 'python-gobject' 'pcsc-tools' 'opensc' 'ccid' 'libusb')
source=(
    "$pkgname-$pkgver.tar.gz::https://github.com/large-farva/cac-manager/archive/refs/heads/main.tar.gz"
    "org.example.CACManager.desktop"
    "org.example.CACManager.png"
)
sha256sums=('SKIP' 'SKIP' 'SKIP')

build() {
    cd "$srcdir/$pkgname-main"
    # No compilation step needed for a Python application
}

package() {
    cd "$srcdir/$pkgname-main"

    # Install main Python script
    install -Dm755 src/main.py "$pkgdir/usr/bin/cac-manager"

    # Install .desktop file
    install -Dm644 org.example.CACManager.desktop "$pkgdir/usr/share/applications/org.example.CACManager.desktop"

    # Install icon
    install -Dm644 org.example.CACManager.png "$pkgdir/usr/share/icons/hicolor/256x256/apps/org.example.CACManager.png"

    # Install README and LICENSE
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
