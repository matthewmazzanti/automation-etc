{ pkgs ? import <nixpkgs> {}, ... }:
with pkgs;
let
  python = python3.withPackages (pyPkgs: with pyPkgs; [
    pylint
  ]);
in pkgs.mkShell {
  buildInputs = with pkgs; [
    python
  ];
}
