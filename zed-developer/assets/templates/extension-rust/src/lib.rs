use zed_extension_api as zed;

struct ExampleExtension;

impl zed::Extension for ExampleExtension {
    fn new() -> Self { Self }
}

zed::register_extension!(ExampleExtension);
