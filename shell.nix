{ pkgs ? import <nixpkgs> {}, ... }:
with pkgs;
let
  aioserial = with python3.pkgs; buildPythonPackage rec {
    pname = "aioserial";
    version = "1.3.0";

    src = fetchPypi {
      inherit pname version;
      sha256 = "080j3ws3j2arj2f16mzqn1qliy0bzmb0gzk5jvm5ldkhsf1s061h";
    };

    propagatedBuildInputs = [ python3.pkgs.pyserial ];

    doCheck = false;
  };

  python = python3.withPackages (pyPkgs: with pyPkgs; [
    pylint
    aiohttp
    aioserial
    evdev
  ]);
in pkgs.mkShell {
  buildInputs = with pkgs; [
    python
  ];
}
