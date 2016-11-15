import java.io.*;
import java.net.Socket;
import java.nio.Buffer;
import java.util.*;

/**
 * Created by Rafael on 15/09/2016.
 */
public class Cliente{

    Scanner sc = new Scanner(System.in);
    private String requisicao = "";
    String chave = "";
    private final String http = "HTTP/1.1";
    String linhaReq = "";
    String respostaServidor = "";
    String corpoTemp = "";
    List<String> corpo = new ArrayList();
    String corpoFinal = "";
    int versao = 0;
    int corpoLen = 0;
    String cabecalho = "";
    Boolean ok = false;
    String lReq = "";
    public static void main(String[] args) throws IOException {
        Cliente x = new Cliente();
        x.run();
    }

    public void run() throws IOException{

        Socket sock = new Socket("127.0.0.1", 5005);// conecta a Sistem de Arquivos
        if (sock.isConnected()) {
            System.out.println("conectou!");
        }
        while (true) {

            InputStream input = sock.getInputStream();
            BufferedReader recebeRequisicao = new BufferedReader(new InputStreamReader(input));
            OutputStream output = sock.getOutputStream();
            PrintStream enviaRequisicao = new PrintStream(output);
            String[] tipoReq;

            while(!ok) {
                System.out.println("Digite o tipo de requisicao (GET, LIST, ADD, UPDATE, DELETE, UPDATE+VERSION, DELETE+VERSION): ");
                lReq = sc.nextLine();
                tipoReq = lReq.split("\\+");

                switch (tipoReq[0]){
                    case "GET":
                        System.out.println("Digite o nome do arquivo: ");
                        chave = sc.nextLine();
                        ok = true;
                        break;
                    case "LIST":
                        System.out.println("Digite o nome do arquivo: ");
                        chave = sc.nextLine();
                        ok = true;
                        break;
                    case "ADD":
//                        lReq = "POST";
                        System.out.println("Digite o nome do arquivo: ");
                        chave = sc.nextLine();
                        System.out.println("Digite o corpo do arquivo: ");
                        corpoTemp = sc.nextLine();
                        while (!corpoTemp.equals("-1")){
                            corpo.add(corpoTemp);
                            corpoTemp = sc.nextLine();
                        }
                        ok = true;
                        break;
                    case "UPDATE":
                        System.out.println("Digite o nome do arquivo: ");
                        chave = sc.nextLine();
                        System.out.println("Digite o corpo do arquivo: ");
                        corpoTemp = sc.nextLine();
                        while (!corpoTemp.equals("-1")){
                            corpo.add(corpoTemp);
                            corpoTemp = sc.nextLine();
                        }
                        ok = true;
                        break;
                    case "DELETE":
                        System.out.println("Digite o nome do arquivo: ");
                        chave = sc.nextLine();
                        ok = true;
                        break;
                    default:
                        System.out.println("Entrada invalida");
                        break;
                }

            }


            linhaReq = lReq +" "+ chave +" "+ http;
            ok = false;

            for (String temp : corpo) {
                corpoLen += temp.length();
                corpoFinal += temp + "\n";

            }
            corpoLen += 1;
            cabecalho = "Host: localhost:5005\n" +
                        "Cache-Control: no-cache\n" +
                        "Content-Length: "+corpoLen;



//            System.out.println("Digite uma requisicao: ");//Pega requisicao
//            while (true) {
//                temp = sc.nextLine();
//                if(temp.equals("end")){
//                    break;
//                }
//                requisicao += temp + "\n";
//            }
//            requisicao = "GET /arq1 HTTP/1.1\n" +
//                    "Host: localhost:5000\n" +
//                    "Cache-Control: no-cache\n" +
//                    "Content-Length: 83\n"+
//                    "Postman-Token: 95096c2d-8bf6-ba68-52a3-dd8ef75e20bb\n" +
//                    "\n" +
//                    "oiee\n" +
//                    "aosdjioasjidaoijsd\n" +
//                    "aoisdodsuhfiusdfisudf\n" +
//                    "iaushdiuashd\n" +
//                    "asdaiusdhiausdhaisd\n" +
//                    "asdf";
            requisicao = linhaReq + "\r\n" + cabecalho +  "\r\n" + "\r\n" + corpoFinal;
            System.out.println(requisicao);
            enviaRequisicao.println(requisicao);
            respostaServidor = recebeRequisicao.readLine();
            while(respostaServidor!= null) {
                System.out.println(respostaServidor);
                respostaServidor = recebeRequisicao.readLine();
            }

            enviaRequisicao.flush();

        }
    }
}
