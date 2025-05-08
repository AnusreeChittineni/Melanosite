import Foundation

class APIManager {
    static let shared = APIManager()
    private let baseUrl = "https://isic-archive.com/api/v1"
    
    func fetchImageMetadata(completion: @escaping (Result<[String: Any], Error>) -> Void) {
        guard let url = URL(string: "\(baseUrl)/image") else { return }
        URLSession.shared.dataTask(with: url) { data, _, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            if let data = data {
                do {
                    let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                    completion(.success(json ?? [:]))
                } catch {
                    completion(.failure(error))
                }
            }
        }.resume()
    }
}