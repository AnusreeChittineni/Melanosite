import UIKit
import Vision
import CoreML

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var resultLabel: UILabel!
    let imagePicker = UIImagePickerController()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        imagePicker.delegate = self
    }
    
    @IBAction func uploadImageTapped(_ sender: UIButton) {
        imagePicker.sourceType = .photoLibrary
        present(imagePicker, animated: true, completion: nil)
    }
    
    @IBAction func captureImageTapped(_ sender: UIButton) {
        if UIImagePickerController.isSourceTypeAvailable(.camera) {
            imagePicker.sourceType = .camera
            present(imagePicker, animated: true, completion: nil)
        } else {
            print("Camera not available")
        }
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        if let selectedImage = info[.originalImage] as? UIImage {
            imageView.image = selectedImage
            processImage(selectedImage)
        }
        dismiss(animated: true, completion: nil)
    }
    
    func processImage(_ image: UIImage) {
        guard let ciImage = CIImage(image: image) else {
            fatalError("Unable to convert UIImage to CIImage")
        }
        
        // Run the model prediction
        MLModelWrapper.shared.runModel(on: ciImage) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let percentage):
                    self?.resultLabel.text = "Likelihood of being cancerous: \(percentage)%"
                case .failure(let error):
                    self?.resultLabel.text = "Error: \(error.localizedDescription)"
                }
            }
        }
    }
}