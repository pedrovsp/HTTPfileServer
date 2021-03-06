package clienteteste;
import java.io.*;
import java.util.*;
import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.*;

public class Cliente{

    static Scanner sc = new Scanner(System.in);
    String chave = "";
    String corpoTemp = "";
    List<String> corpo = new ArrayList<String>();
    String corpoFinal = "";
    int versao = 0;
    Boolean ok = true;
    String lReq = "";
    String resposta = "";
    TTransport transport;
    static int porta;

    public static void main(String[] args) throws IOException {
        //porta = Integer.parseInt(args[1]);
        System.out.println("Digite a porta");
        porta = Integer.parseInt(sc.nextLine());
        sc.reset();
        Cliente x = new Cliente();
        x.run();
    }

    public void run() throws IOException{

        try
        {
            transport = new TSocket("127.0.0.1", porta);
            transport.open();
            TProtocol protocol = new TBinaryProtocol(transport);
            RequestHandler.Client client = new RequestHandler.Client(protocol);

            while (true) 
            {
                String[] tipoReq;

                while(ok) 
                {
                    System.out.println("Digite o tipo de requisicao (GET, LIST, ADD, UPDATE, DELETE, UPDATE+VERSION, DELETE+VERSION): ");
                    lReq = sc.nextLine();
                    tipoReq = lReq.split("\\+");

                    switch (tipoReq[0])
                    {
                        case "GET":
                            System.out.println("Digite o nome do arquivo: ");
                            chave = sc.nextLine();
                            resposta = client.do_get(chave);
                            break;
                        case "LIST":
                            System.out.println("Digite o nome do arquivo: ");
                            chave = sc.nextLine();
                            resposta = client.do_list(chave);
                            break;
                        case "ADD":
                            System.out.println("Digite o nome do arquivo: ");
                            chave = sc.nextLine();
                            System.out.println("Digite o corpo do arquivo: ");
                            corpoTemp = sc.nextLine();
                            while (!corpoTemp.equals("-1")){
                                corpo.add(corpoTemp);
                                corpoTemp = sc.nextLine();
                            }
                            for (String temp : corpo) {
                                corpoFinal += temp + "\n";
                            }
                            resposta = client.do_add(corpoFinal, chave, null);
                            corpoFinal = "";
                            break;
                        case "UPDATE":
                            System.out.println("Digite o nome do arquivo: ");
                            chave = sc.nextLine();
                            System.out.println("Digite o corpo do arquivo: ");
                            corpoTemp = sc.nextLine();
                            while (!corpoTemp.equals("-1"))
                            {
                                corpo.clear();
                                corpo.add(corpoTemp);
                                corpoTemp = sc.nextLine();
                            }
                            
                            for (String temp : corpo) 
                            {
                                corpoFinal += temp + "\n";
                            }
                            resposta = client.do_update(corpoFinal, chave, null);
                            corpoFinal = "";
                            break;
                        case "UPDATE_VERSION":
                            System.out.println("Digite o nome do arquivo: ");
                            chave = sc.nextLine();
                            System.out.println("Digite a versao do arquivo: ");
                            versao = sc.nextInt();
                            System.out.println("Digite o corpo do arquivo: ");
                            corpoTemp = sc.nextLine();
                            while (!corpoTemp.equals("-1"))
                            {
                                corpo.clear();
                                corpo.add(corpoTemp);
                                corpoTemp = sc.nextLine();
                            }
                            
                            for (String temp : corpo) 
                            {
                                corpoFinal += temp + "\n";
                            }
                            resposta = client.do_update_version(corpoFinal, versao, chave, null);
                            corpoFinal = "";
                            break;
                        case "DELETE_VERSION":
                            System.out.println("Digite o nome do arquivo: ");
                            chave = sc.nextLine();
                            System.out.println("Digite a versao do arquivo: ");
                            versao = sc.nextInt();
                            resposta = client.do_delete_version(chave, versao);
                            break;
                        case "DELETE":
                            System.out.println("Digite o nome do arquivo: ");
                            chave = sc.nextLine();
                            resposta = client.do_delete(chave);
                            break;
                        case "exit":
                            transport.close();
                            ok = false;
                            resposta = "Fehcando cliente";
                            break;
                        default:
                            System.out.println("Entrada invalida");
                            break;
                    }
                    sc.reset();
                    System.out.println(resposta);
                }
                break;
            }
        } 
        catch (TException x) 
        {
            x.printStackTrace();
        }
    }
}
