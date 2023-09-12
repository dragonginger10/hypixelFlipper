{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
    in {
      formatter = pkgs.alejandra;

      devShells.default = pkgs.mkShell {
        packages = with pkgs;
          [python3]
          ++ (with pkgs.python3Packages; [pip requests typer python-dotenv rich pandas black isort]);
      };

      packages = rec {
        default = flipper;

        flipper = with pkgs.python310Packages;
          buildPythonApplication {
            pname = "flipper";
            version = "0.1";
            format = "pyproject";

            propagatedBuildInputs = [setuptools requests typer rich pandas];

            src = ./.;
          };
      };
    });
}
