; Example program to demonstrate file I/O.
; This example will open/create a file, write some ; information to the file, and close the file.
; Note, the file name is hard­coded for this example.
; This example program will open a file, read the ; contents, and write the contents to the screen.
; This routine also provides some very simple examples ; regarding handling various errors on system services.
;­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­


section .data


; ­­­­­
;  Define standard constants.

LF equ 10 
NULL equ 0

TRUE equ 1
FALSE equ 0
EXIT_SUCCESS equ 0

STDIN equ 0
STDOUT equ 1
STDERR equ 2

SYS_read equ 0
SYS_write equ 1
SYS_open equ 2
SYS_close equ 3
SYS_fork equ 57
SYS_exit equ 60
SYS_creat equ 85
SYS_time equ 201

O_CREAT equ 0x40
O_TRUNC equ 0x200
O_APPEND equ 0x400

O_RDONLY equ 000000q
O_WRONLY equ 000001q
O_RDWE equ 000002q

S_IRUSR equ 00400q
S_IWUSR equ 00200q
S_IXUSR equ 00100q

; ­­­­­
;  Variables/constants for main.

BUFF_SIZE equ 255
newLine db LF,NULL
header db LF,"File Read Example."
       db LF,LF,NULL
fileName db "url.txt",NULL
fileDescriptor dw 0
errMsgOpen db "Error opening the file.",LF,NULL
errMsgRead db "Error reading from the file.",LF,NULL
;­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­
section .bss
readBuffer resb BUFF_SIZE
;­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­

section .text 
global main 
main:
; ­­­­­
;  Display header line...
  mov rdi, header
  call printString

; ­­­­­
; Attempt to open file.
; Use system service for file open
; System Service ­ Open
; rax = SYS_open
; rdi = address of file name string
; rsi = attributes (i.e., read only, etc.) ; Returns:
; iferror­>eax<0
; if success ­> eax = file descriptor number
; The file descriptor points to the File Control Block (FCB).
; The FCB is maintained by the OS.
; The file descriptor is used for all subsequent file
; operations (read, write, close).

;;
openInputFile:
        mov qword [fileDescriptor],rax
	mov rax, SYS_open 
	mov rdi, fileName 
	mov rsi, O_RDONLY 	
	syscall
	cmp rax, 0
        jl errorOnOpen
        ; file open
        ; file name string
        ; read only access
        ; call the kernel
        ; check for success
        mov qword [fileDescriptor], rax ; save descriptor
; ­­­­­
; Read from file.
; In this example, we know that the file has exactly 1 line.
;  System Service ­ Read
; rax = SYS_read
; rdi = file descriptor
; rsi = address of where to place data
; rdx = count of characters to read
; Returns:
; iferror­>rax<0
; if success ­> rax = count of characters actually read
        mov rax, SYS_read
        mov rdi, qword [fileDescriptor]
        mov rsi, readBuffer
        mov rdx, BUFF_SIZE
        syscall
        cmp rax,0
        jl errorOnRead


; ­­­­­
; Print the buffer.
; add the NULL for the print string
        mov rsi, readBuffer
        mov byte [rsi+rax], NULL
        mov rdi, readBuffer
        call printString
        printNewLine
; ­­­­­
;  Close the file.
;  System Service ­ close
; rax = SYS_close
; rdi = file descriptor
        mov rax, SYS_close
        mov rdi, qword [fileDescriptor]
        syscall
        jmp exampleDone


; ­­­­­
; Error on open.
; note, eax contains an error code which is not used ; for this example.
errorOnOpen:
        mov rdi, errMsgOpen
        call printString
        jmp exampleDone
; ­­­­­
; Error on read.
; note, eax contains an error code which is not used ; for this example.
errorOnRead:
        mov rdi, errMsgRead
        call printString
        jmp exampleDone

; ­­­­­

; Generic procedure to display a string to the screen.
; String must be NULL terminated.
; Algorithm:
; Count characters in string (excluding NULL)
; Use syscall to output characters
; Arguments:
; 1) address, string ; Returns:
; nothing
global printString
printString:
        push rbp
        mov rbp, rsp
        push rbx

; ­­­­­
;  Count characters in string.
mov rbx, rdi
mov rdx, 0
strCountLoop:
        cmp byte [rbx], NULL
        je strCountDone
        inc rdx
        inc rbx
        jmp strCountLoop
strCountDone:
        cmp rdx, 0
        je prtDone

; ­­­­­
;  Call OS to output string.
        mov eax, SYS_write  ; code for write()
        mov rsi, rdi        ; addr of characters
        mov rdi, STDOUT     ; file descriptor
        syscall
; count set above
; system call
; ­­­­­
; String printed, return to calling routine.
prtDone:
        pop rbx
        pop rbp
        ret

; ­­­­­
;  Example program done.
exampleDone:
        mov rax, SYS_exit
        mov rbx, EXIT_SUCCESS
        syscall
