[TOC]

# README: Getting Started with TCP #

## Hello World Example ##

Single machine TCP or UDP:

1. Run TCPServer.java first, then TCPClient.java on the same machine. For UDP, run the corresponding files UDPServer.java and UDPClient.java.
2. Verify that that the "capitalizing" server returns capitalized user input as expected.

Multiple machines: If you have access another physical machine or a virtual machine, you can verify that the above code works exactly as above across a network provided you change the name or IP address of the server in the client from `localhost` to that of the server.

The simple java example code above doesn't quite illustrate TCP's bytestream abstraction because it hides it underneath the `readLine` method. The corresponding python TCPServer/TCPClient example is technically incorrect (or at least incomplete) because the `read` method assumes that everything that was sent by the other side has been received and read. TCP's bytestream abstraction is the reason why that assumption is incorrect. Read on below to understand it better.

## Bytestream ##

Unlike UDP's (unreliable) datagram abstraction that either delivers all of a datagram or none of a datagram, TCP reliably delivers transmitted bytes in order to the receiver but may do so in arbitrary sized chunks, e.g., if the sender sends "*I saw a puppy*", the receiver TCP upon the first socket read may just read the first four bytes "I sa" for one or both of two possible reasons:

* those are all of the bytes that have arrived up until then; or 
* the size of the array into which the receiver is reading those bytes is of capacity 4;

In either case, the remaining bytes are following right behind or have already arrived into the receiver socket just waiting to be read. In general, issuing a TCP read from a socket into a byte array of size N does not mean that the read will return N bytes even if the sender from the other end has sent at least N bytes, rather the read will block until it has read at least one byte and may return any number of bytes between 1 and N. The only guarantee TCP makes is of a *reliable bytestream*, i.e., the bytes will be read off the socket in the order sent by the sender and all bytes sent will *eventually* arrive.

To be able to better appreciate TCP's bytestream abstraction:

1. Start TCPServerByteArray.java, and then TCPClient.java as before.
2. Type a long sentence or cut-paste contents of a file into standard input on the client side.
3. Observe how the server side "trickles" in the bytestream as and when the bytes arrive and are read by the receiver.

## Other examples ##

Next, run the following pairs of server/client programs and verify that they behave as expected.

`PersistentTCPServer.java, PersistentTCPClient.java`: The simple server examples above dealt with exactly one client request at a time before attending to the next client. Refer to the structure of the main `while` loop to observe as much. The `PersistentTCP*` files allow the server to deal with multiple client requests from a single client before moving on to the next client.

`ThreadedPersistentTCPServer.java, PersistentTCPClient.java`: This example extends the previous example to allow multiple clients to be serviced concurrently each being able to send an arbitrary number of requests before quitting.