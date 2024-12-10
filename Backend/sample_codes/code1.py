public class DeleteFileProgram {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the name of the file to delete: ");
        String filename = scanner.nextLine();

        File file = new File(filename);
        if (file.delete()) {
            System.out.println("File deleted successfully.");
        } else {
            System.out.println("File not found or could not be deleted.");
        }
    }
}
