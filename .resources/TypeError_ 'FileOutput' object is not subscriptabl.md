<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# TypeError: 'FileOutput' object is not subscriptable replicate download output

Based on your previous interest in using the Replicate API for image generation, the error `TypeError: 'FileOutput' object is not subscriptable` indicates a change in how the Replicate Python client library handles outputs[^11]. This error typically occurs when you try to access the result of a `replicate.run()` call using an index, like `output`, which is a method for lists, not the `FileOutput` object that is now returned[^2].

With the release of version 1.0.0 of the Replicate client library, models that generate files like images no longer return a list of URLs. Instead, `replicate.run()` returns `FileOutput` objects, which provide direct access to the file data[^2][^4].

### Understanding and Fixing the Error

The error arises because your code expects a list (which is "subscriptable," meaning you can access its elements with `[index]`) but receives a single `FileOutput` object instead.

To fix this, you should interact with the `FileOutput` object using its methods, such as `.read()` to get the file's binary content or its `.url` property to get the temporary URL[^2].

### How to Handle `FileOutput` Objects

Here are the correct ways to download an image or access its URL from the `replicate.run()` output.

**Downloading a Single Image**
If the model returns a single file, the output will be one `FileOutput` object. You can use its `.read()` method to get the content and write it to a local file[^3].

```python
import replicate

# This call returns a FileOutput object, not a list
output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={"prompt": "A majestic lion"}
)

# Use the .read() method to get the binary data and save the image
with open('output.png', 'wb') as f:
    f.write(output.read())

print("Image saved as output.png")
```

**Handling Multiple Image Outputs**
If you configure the model to generate multiple outputs, `replicate.run()` will return an iterator of `FileOutput` objects. You should loop through this iterator to save each file[^2].

```python
import replicate

# This call returns an iterator of FileOutput objects
output = replicate.run(
    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    input={"prompt": "Two astronauts planting a flag on Mars", "num_outputs": 2}
)

# Iterate through the outputs to save each image
for idx, file_output in enumerate(output):
    with open(f'output_{idx}.png', 'wb') as f:
        f.write(file_output.read())
    print(f"Image output_{idx}.png saved.")
```

**Accessing the Image URL**
If you need the image URL instead of the file itself (for example, to display it in a web application), you can access the `.url` property of the `FileOutput` object[^2].

It is important to note that these URLs are temporary and will expire after one hour. They are served from `replicate.delivery`[^2][^4].

```python
import replicate

output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={"prompt": "A majestic lion"}
)

# Access the .url attribute to get the temporary URL
image_url = output.url
print(f"File available at: {image_url}")
```

<div style="text-align: center">⁂</div>

[^1]: https://github.com/simonw/llm-replicate/issues/22

[^2]: https://replicate.com/docs/topics/predictions/output-files

[^3]: https://replicate.com/docs/get-started/python

[^4]: https://replicate.com/docs/reference/how-does-replicate-work

[^5]: https://stackoverflow.com/questions/7896910/why-is-this-saying-that-the-object-is-not-subscriptable-python

[^6]: https://stackoverflow.com/questions/56796485/how-to-fix-typeerror-type-object-is-not-subscriptable/56796512

[^7]: https://learn.microsoft.com/en-us/answers/questions/1291639/typeerror-type-object-is-not-subscriptable-while-s

[^8]: https://github.com/replicate/replicate-python/blob/main/README.md

[^9]: https://www.reddit.com/r/learnpython/comments/vbgyz5/what_does_this_error_mean_by_this_object_is_not/

[^10]: https://learn.microsoft.com/en-us/answers/questions/607701/getting-exception-typeerror-function-object-is-not

[^11]: programming.api_integration

