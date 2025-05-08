import CoreML
import Vision
import UIKit

class MLModelWrapper {
    static let shared = MLModelWrapper()
    private var model: VNCoreMLModel?
    
    private init() {
        guard let coreMLModel = try? SkinLesionClassifier(configuration: .init()).model else {
            fatalError("Failed to load Core ML model")
        }
        model = try? VNCoreMLModel(for: coreMLModel)
    }
    
    func runModel(on image: CIImage, completion: @escaping (Result<Double, Error>) -> Void) {
        guard let model = model else {
            completion(.failure(NSError(domain: "MLModelError", code: -1, userInfo: [NSLocalizedDescriptionKey: "Model not loaded"])))
            return
        }
        
        let request = VNCoreMLRequest(model: model) { request, error in
            if let results = request.results as? [VNClassificationObservation],
               let topResult = results.first {
                completion(.success(Double(topResult.confidence * 100)))
            } else if let error = error {
                completion(.failure(error))
            } else {
                completion(.failure(NSError(domain: "MLModelError", code: -2, userInfo: [NSLocalizedDescriptionKey: "No results"])))
            }
        }
        
        let handler = VNImageRequestHandler(ciImage: image, options: [:])
        DispatchQueue.global(qos: .userInteractive).async {
            do {
                try handler.perform([request])
            } catch {
                completion(.failure(error))
            }
        }
    }
}
