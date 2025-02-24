
{ pkgs }: {
  deps = [
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.libxcrypt
    pkgs.python39
    pkgs.libuuid
    pkgs.alsa-lib
    pkgs.libpulseaudio
  ];
}
