create database db_escola;

--------------------------------------------------------------------
create table tbl_professores(
       pro_codigo int primary key auto_increment,
       pro_nome varchar(255),
       pro_endereco varchar(255),
       pro_email varchar(255),
       pro_telefone int,
       pro_cpf int,
       pro_nascimento varchar(255));
       
alter table tbl_professores
add column cid_codigo int,
add constraint fk_cid_codigo foreign key (cid_codigo)
references tbl_cidade(cid_codigo);

--------------------------------------------------------------------

create table tbl_alunos(
       alu_codigo int primary key auto_increment,
       alu_nome varchar(255),
       alu_endereco varchar(255),
       alu_email varchar(255),
       alu_telefone int,
       alu_nascimento varchar(255));
       
alter table tbl_alunos
add column cid_codigo int,
add constraint fk_cida_codigo foreign key (cid_codigo)
references tbl_cidade(cid_codigo);
        
alter table tbl_alunos
add column cur_codigo int,
add constraint fk_cur_codigo foreign key (cur_codigo)
references tbl_curso(cur_codigo);
        
--------------------------------------------------------------------        

create table tbl_cidade(
       cid_codigo int primary key auto_increment,
       cid_nome varchar(255),
       cid_uf varchar(255));       
       
--------------------------------------------------------------------    
       
create table tbl_curso(
       cur_codigo int primary key auto_increment,
       cur_nome varchar(255),
       cur_valor int );
    
--------------------------------------------------------------------
       
create table tbl_usuario(
       usu_codigo int primary key auto_increment,
       usu_nome varchar(255),
       usu_username varchar(255),
       usu_senha varchar(255));
      
--------------------------------------------------------------------

create table tbl_aulas(
       aul_codigo int primary key auto_increment, 
       aul_horario varchar(255),
       aul_sala varchar(255));

alter table tbl_aulas
add column cur_codigo int,
add constraint fk_curs_codigo foreign key (cur_codigo)
references tbl_curso(cur_codigo);

alter table tbl_aulas
add column alu_codigo int,
add constraint fk_alu_codigo foreign key (alu_codigo)
references tbl_alunos(alu_codigo)

alter table tbl_aulas
add column pro_codigo int,
add constraint fk_pro_codigo foreign key (pro_codigo)
references tbl_professores(pro_codigo)