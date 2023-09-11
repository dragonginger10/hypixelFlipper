{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { self
    , nixpkgs
    , flake-utils
    }:

    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [ python3 ] ++
          (with pkgs.python3Packages; [ pip requests typer python-dotenv rich ]);
      };

      packages.default = with pkgs.python3Packages;
        buildPythonApplication {
          pname = "flipper";
          version = "0.1";
          format = "pyproject";

          propagatedBulidInputs = [ setuptools requests typer rich python-dotenv];

          src = ./.;
        };
    });
}
