create schema if not exists rh;
create schema instituicao;
create schema geo;
create schema inscricao;

create table if not exists rh.pessoa (
    id serial primary key,
    nome text not null,
    dt_nascimento date not null,
    email text not null unique,
    created_at timestamp default current_timestamp,
    updated_at timestamp,
    bo_ativo boolean default true
);

create table if not exists rh.documento_tipo (
    id serial primary key,
    ds_documento text not null
);

create table if not exists rh.documento (
    id serial primary key,
    id_pessoa int not null,
    id_documento_tipo int not null,
    numero text not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp,
    bo_ativo boolean default true,
    constraint fk_documento_tipo foreign key (id_documento_tipo) references rh.documento_tipo(id),
    constraint fk_documento_pessoa foreign key (id_pessoa) references rh.pessoa(id),
    constraint uq_documento_tipo_numero unique (id_documento_tipo, numero)
);

create table if not exists rh.telefone (
    id serial primary key,
    telefone text not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp
);

create table if not exists rh.pessoa_telefone (
    id serial primary key,
    id_pessoa int not null,
    id_telefone int not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp,
    bo_ativo boolean default true,
    constraint fk_pessoa_telefone foreign key (id_pessoa) references rh.pessoa(id),
    constraint fk_telefone_pessoa foreign key (id_telefone) references rh.telefone(id),
    constraint uq_pessoa_telefone unique (id_pessoa, id_telefone)
);

create table if not exists rh.usuario (
    id int primary key,
    numero_cpf text not null,
    senha text not null,
    bo_ativo boolean default false,
    created_at timestamp default current_timestamp,
    updated_at timestamp,
    constraint fk_usuario_pessoa foreign key (id) references rh.pessoa(id) on delete cascade
);

create table if not exists rh.perfil_tipo (
    id serial primary key,
    ds_perfil text not null,
    bo_ativo boolean default true
);

create table if not exists rh.usuario_perfil (
    id serial primary key,
    id_usuario int not null,
    id_perfil int not null,
    created_at timestamp default current_timestamp,
    bo_ativo boolean default true,
    constraint fk_usuario_perfil_usuario foreign key (id_usuario) references rh.usuario(id),
    constraint fk_usuario_perfil_perfil foreign key (id_perfil) references rh.perfil_tipo(id),
    constraint uq_usuario_perfil unique (id_usuario, id_perfil)
);

create table if not exists geo.estados (
    id serial not null,
    codigo_uf text not null,
    nome text not null,
    uf text not null,
    bo_ativo bool default true,
    constraint estado_pkey primary key (id)
);

create table if not exists geo.municipio (
    id serial primary key,
    no_municipio text not null,
    uf char(2) not null,
    cod_ibge text not null,
    bo_ativo boolean default true,
    created_at timestamp default current_timestamp,
    updated_at timestamp
);

create table if not exists geo.municipios (
  id serial4 not null,
  codigo_municipio text not null,
  nome text not null,
  id_estado int4 not null
);

do $$
begin
  if not exists (select 1 from pg_constraint where conname = 'municipio_pkey') then
    alter table geo.municipios add constraint municipio_pkey primary key (id);
  end if;
  if not exists (select 1 from pg_constraint where conname = 'fk_estados') then
    alter table geo.municipios add constraint fk_estados foreign key (id_estado) references geo.estados(id);
  end if;
end $$;

create table instituicao.campus (
    id serial primary key,
    id_municipio int not null,
    no_campus text not null,
    bo_ativo boolean default true,
    created_at timestamp default current_timestamp,
    updated_at timestamp,
    constraint fk_municipio foreign key (id_municipio) references geo.municipio(id)
);

create table instituicao.curso (
    id serial primary key,
    no_curso text not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp,
    bo_ativo boolean default true
);

create table instituicao.curso_campus (
    id serial primary key,
    id_campus int not null,
    id_curso int not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp,
    bo_ativo boolean default true,
    constraint fk_curso_campus_campus foreign key (id_campus) references instituicao.campus(id),
    constraint fk_curso_campus_curso foreign key (id_curso) references instituicao.curso(id)
);

create table if not exists inscricao.evento (
    id serial primary key,
    titulo varchar(255) not null,
    descricao text not null,
    dt_inicio date not null,
    dt_fim date not null,
    id_criador int not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp,
    bo_ativo boolean default true,
    constraint fk_evento_criador foreign key (id_criador) references rh.pessoa(id)
);

create table if not exists inscricao.evento_inscricao (
    id serial primary key,
    id_evento int not null,
    id_pessoa int not null,
    created_at timestamp default current_timestamp,
    bo_ativo boolean default true,
    constraint fk_evento_inscricao_evento foreign key (id_evento) references inscricao.evento(id),
    constraint fk_evento_inscricao_pessoa foreign key (id_pessoa) references rh.pessoa(id),
    constraint uq_evento_pessoa unique (id_evento, id_pessoa)
);

create index idx_pessoa_email on rh.pessoa(email);
create index idx_documento_id_pessoa on rh.documento(id_pessoa);
create index idx_documento_id_documento_tipo on rh.documento(id_documento_tipo);
create index idx_pessoa_telefone_id_pessoa on rh.pessoa_telefone(id_pessoa);
create index idx_usuario_numero_cpf on rh.usuario(numero_cpf);
create index idx_municipio_uf on geo.municipio(uf);
create index idx_municipio_cod_ibge on geo.municipio(cod_ibge);
create index idx_campus_id_municipio on instituicao.campus(id_municipio);
create index idx_curso_campus_id_curso on instituicao.curso_campus(id_curso);
create index idx_curso_campus_id_campus on instituicao.curso_campus(id_campus);
create index idx_evento_id_criador on inscricao.evento(id_criador);
create index idx_evento_inscricao_id_evento on inscricao.evento_inscricao(id_evento);
create index idx_evento_inscricao_id_pessoa on inscricao.evento_inscricao(id_pessoa);

