import UIKit

class ImageProcessor {
    static func preprocessImage(_ image: UIImage) -> UIImage? {
        let targetSize = CGSize(width: 224, height: 224) // Resize image to match ML model input
        UIGraphicsBeginImageContextWithOptions(targetSize, true, 0.0)
        image.draw(in: CGRect(origin: .zero, size: targetSize))
        let resizedImage = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        return resizedImage
    }
}
