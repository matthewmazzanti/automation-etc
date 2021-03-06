{ pkgs ? import <nixpkgs> {} }:
with pkgs;
python3Packages.buildPythonApplication rec {
  pname = "room";
  version = "&&VERSION";
  src = ./.;
  propagatedBuildInputs = [];
  meta = {
    description = "&&DESCRIPTION&&";
  };
}
