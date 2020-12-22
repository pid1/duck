# duck
An HTML-based URL shortener for static sites. 🦆

## Usage

`./quack.py <url>` dump out a small HTML file that contains a meta tag with a Refresh element and target URL. This will redirect browsers to the provided target URL. The filename is the shorturl of the target resource. 

By updating `duck.toml` with the directory containing your Github Pages site (or any other static site), you can use this to quickly generate short URLs for web resources with no nonsense, no tracking, and no credit card required.

You can also configure the slug length by updating `duck.toml`.

## Improvements

* Implement a small os.walk function and some regex to check and see if we have an existing slug that points to the provided target URL.
* Instead of bailing out, simply regenerate the slug until we find one that has not been used. Implement a base case based on the configured maximum slug length so we don't loop forever.
* Make the slug length a maximum potential length, not hardcoded length, to increase our pool of available slugs.